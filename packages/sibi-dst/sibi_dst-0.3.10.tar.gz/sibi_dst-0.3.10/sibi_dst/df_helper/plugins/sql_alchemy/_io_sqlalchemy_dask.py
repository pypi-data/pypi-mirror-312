import itertools
import dask.dataframe as dd
import pandas as pd
from sqlalchemy.orm import Query
from sqlalchemy.inspection import inspect


class ReadFrameSqlAlchemy:
    def __init__(
        self,
        query,
        session,
        fieldnames=None,
        index_col=None,
        coerce_float=False,
        verbose=True,
        datetime_index=False,
        column_names=None,
        chunk_size=1000,
    ):
        """
        Initialize the loader for SQLAlchemy queries.

        Args:
            query: SQLAlchemy query (ORM or Select).
            session: SQLAlchemy session for executing the query.
            fieldnames: Optional list of field names to include in the result.
            index_col: Column to use as the index of the DataFrame.
            coerce_float: Attempt to coerce values to float where applicable.
            verbose: Whether to include verbose processing like handling choices.
            datetime_index: Whether to convert the index to a datetime index.
            column_names: Optional mapping of fieldnames to custom column names.
            chunk_size: Number of records to fetch in each chunk.
        """
        self.query = query
        self.session = session
        self.fieldnames = fieldnames
        self.index_col = index_col
        self.coerce_float = coerce_float
        self.verbose = verbose
        self.datetime_index = datetime_index
        self.column_names = column_names
        self.chunk_size = chunk_size

    @staticmethod
    def row_to_dict(row, fields=None):
        """
        Convert a SQLAlchemy result row to a dictionary.

        Args:
            row: SQLAlchemy ORM object, Row object, or tuple.
            fields: List of fields to extract.

        Returns:
            A dictionary representation of the row.
        """
        # Handle ORM instances
        if hasattr(row, "__dict__"):  # For ORM instances
            data = row.__dict__.copy()
            data.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal state
        # Handle SQLAlchemy Row objects
        elif hasattr(row, "_mapping"):  # For SQLAlchemy result rows
            data = dict(row._mapping)
        # Handle tuples (e.g., raw query results)
        elif isinstance(row, tuple):
            if fields:
                data = dict(zip(fields, row))
            else:
                raise ValueError("Cannot map tuple row without field names.")
        else:
            raise ValueError(f"Unsupported row type: {type(row)}. Expected ORM instance, dict-like object, or tuple.")

        # Filter by specified fields
        if fields:
            return {field: data.get(field, None) for field in fields}
        else:
            return data

    def read_frame(self, fillna_value=None):
        """
        Convert the query results to a Dask DataFrame.

        Args:
            fillna_value: Value to use for filling missing values.

        Returns:
            A Dask DataFrame.
        """
        # Infer fieldnames if not provided
        if not self.fieldnames:
            if hasattr(self.query, "selected_columns"):
                self.fieldnames = [col.key for col in self.query.selected_columns]
            else:
                self.fieldnames = [col.name for col in inspect(self.query._entity_zero().class_).columns]

        partitions = []
        results = self.session.execute(self.query)  # Execute the query

        # Debugging raw results
        print("Results fetched:", results)

        # Chunk processing
        iterator = iter(results)
        while True:
            chunk = list(itertools.islice(iterator, self.chunk_size))
            if not chunk:
                break

            # Convert chunk to DataFrame
            df = pd.DataFrame.from_records(
                [self.row_to_dict(row, self.fieldnames) for row in chunk],
                columns=self.fieldnames,
                coerce_float=self.coerce_float,
            )

            # Handle missing values
            if fillna_value is not None:
                df = df.fillna(fillna_value)

            # Convert datetime columns to timezone-naive
            for col in df.columns:
                if isinstance(df[col].dtype, pd.DatetimeTZDtype):
                    df[col] = df[col].dt.tz_localize(None)

            partitions.append(dd.from_pandas(df, npartitions=1))

        # Concatenate partitions
        dask_df = dd.concat(partitions, axis=0, ignore_index=True)

        # Handle index column
        if self.index_col and self.index_col in dask_df.columns:
            dask_df = dask_df.set_index(self.index_col)

        # Convert index to datetime if required
        if self.datetime_index and self.index_col in dask_df.columns:
            dask_df = dask_df.map_partitions(lambda df: df.set_index(pd.to_datetime(df.index)))

        # Handle column renaming
        if self.column_names:
            rename_mapping = dict(zip(self.fieldnames, self.column_names))
            dask_df = dask_df.rename(columns=rename_mapping)

        return dask_df