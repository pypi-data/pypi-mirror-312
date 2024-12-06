import pandas as pd
import dask.dataframe as dd
from sibi_dst.utils import Logger

class DataUtils:

    def __init__(self, logger=None):
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    @staticmethod
    def transform_numeric_columns(df, columns=None, fill_value=0, transform_func=None):
        """
        Transform numeric columns in a DataFrame (Pandas or Dask), handling missing values and applying optional transformations.

        Parameters:
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.
        - fill_value (int or float): The value to replace NA values with.
        - transform_func (callable, optional): The transformation function to apply.
          If None, no additional transformation is applied.

        Returns:
        - pandas.DataFrame or dask.dataframe.DataFrame: Updated DataFrame with transformed numeric columns.
        """
        if columns is None:
            # Detect numeric columns
            columns = df.select_dtypes(include=['number']).columns.tolist()

        if not columns:
            return df

        # Default transformation function (identity) if none is provided
        if transform_func is None:
            transform_func = lambda x: x

        # Apply transformations
        for col in columns:
            dtype = df[col].dtype
            if pd.api.types.is_integer_dtype(dtype):
                meta_type = 'int64'
            elif pd.api.types.is_float_dtype(dtype):
                meta_type = 'float64'
            else:
                continue  # Skip non-numeric columns

            df[col] = df[col].fillna(fill_value).astype(meta_type)
            if isinstance(df, dd.DataFrame):
                df[col] = df[col].map_partitions(
                    lambda s: s.apply(transform_func), meta=(col, meta_type)
                )
            else:
                df[col] = df[col].apply(transform_func)
        return df

    @staticmethod
    def transform_boolean_columns(df, columns=None, sample_size=100):
        """
        Detect if the provided columns in a DataFrame (Pandas or Dask) contain only 0 and 1
        and convert them to boolean. Detection is performed using a sample.

        Parameters:
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.
        - columns (list of str): List of columns to check and transform.
        - sample_size (int): Number of rows to sample for detection. Ignored for Pandas DataFrames.

        Returns:
        - pandas.DataFrame or dask.dataframe.DataFrame: Updated DataFrame with transformed boolean columns.
        """
        # Apply transformation to each specified column
        for col in columns:
            if col in df.columns:
                if isinstance(df, dd.DataFrame):
                    # Replace NaN with 0, then convert to boolean
                    df[col] = df[col].map_partitions(
                        lambda s: pd.to_numeric(s, errors='coerce')  # Convert to numeric, invalid to NaN
                        .fillna(0)  # Replace NaN with 0
                        .astype(int)  # Ensure integer type
                        .astype(bool),  # Convert to boolean
                        meta=(col, 'bool')
                    )
                else:
                    # For Pandas DataFrame, handle mixed types and invalid values
                    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, invalid to NaN
                    df[col] = df[col].fillna(0).astype(int).astype(bool)

        return df

    def merge_lookup_data(self, classname, df, **kwargs):
        """
        Merge lookup data into the DataFrame based on specified columns.

        Parameters:
        - classname: The class instance to use for loading lookup data.
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.
        - kwargs: Additional keyword arguments for configuration.

        Returns:
        - pandas.DataFrame or dask.dataframe.DataFrame: Updated DataFrame with merged lookup data.
        """
        # Check if the DataFrame is empty
        if self.is_dataframe_empty(df):
            return df

        # Extract required parameters with default values
        source_col = kwargs.pop('source_col', None)
        lookup_col = kwargs.pop('lookup_col', None)
        lookup_description_col = kwargs.pop('lookup_description_col', None)
        source_description_alias = kwargs.pop('source_description_alias', None)
        fillna_source_description_alias = kwargs.pop('fillna_source_description_alias', False)
        fieldnames = kwargs.get('fieldnames', None)
        column_names = kwargs.get('column_names', None)

        # Validate required parameters
        if not all([source_col, lookup_col, lookup_description_col, source_description_alias]):
            raise ValueError(
                'source_col, lookup_col, lookup_description_col, and source_description_alias must be specified'
            )

        if source_col not in df.columns:
            self.logger.info(f'{source_col} not in DataFrame columns')
            return df

        # Get unique IDs from source column
        ids = df[source_col].dropna().unique()
        if isinstance(ids, dd.Series):
            ids = ids.compute()
        ids = ids.tolist()

        if not ids:
            self.logger.info(f'No IDs found in the source column: {source_col}')
            return df

        # Set default fieldnames and column_names if not provided
        if fieldnames is None:
            kwargs['fieldnames'] = (lookup_col, lookup_description_col)
        if column_names is None:
            kwargs['column_names'] = ['temp_join_col', source_description_alias]

        # Prepare kwargs for loading lookup data
        load_kwargs = kwargs.copy()
        load_kwargs[f'{lookup_col}__in'] = ids

        # Load lookup data
        lookup_instance = classname()
        result = lookup_instance.load(**load_kwargs)

        # Determine the join column on the result DataFrame
        if 'temp_join_col' in kwargs.get("column_names", []):
            temp_join_col = 'temp_join_col'
        else:
            temp_join_col = lookup_col

        # Merge DataFrames
        df = df.merge(result, how='left', left_on=source_col, right_on=temp_join_col)

        if fillna_source_description_alias and source_description_alias in df.columns:
            df[source_description_alias] = df[source_description_alias].fillna('')

        # Drop temp_join_col if present
        if 'temp_join_col' in df.columns:
            df = df.drop(columns='temp_join_col')

        return df

    @staticmethod
    def is_dataframe_empty(df):
        """
        Check if a DataFrame (Pandas or Dask) is empty.

        Parameters:
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.

        Returns:
        - bool: True if the DataFrame is empty, False otherwise.
        """
        if isinstance(df, dd.DataFrame):
            df_size = df.map_partitions(len).sum().compute()
            return df_size == 0
        else:
            return df.empty

    @staticmethod
    def convert_to_datetime(df, date_fields):
        for col in date_fields:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df