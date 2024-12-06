import dask.dataframe as dd
import pandas as pd
from django.db.models import Q

from sibi_dst.df_helper.plugins.django import ReadFrameDask
from sibi_dst.utils import Logger

class DjangoLoadFromDb:
    df: dd.DataFrame

    def __init__(self, db_connection, db_query, db_params, logger, **kwargs):
        self.connection_config = db_connection
        self.debug = kwargs.pop('debug', False)
        self.verbose_debug = kwargs.pop('verbose_debug', False)
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)
        if self.connection_config.model is None:
            if self.debug:
                self.logger.critical('Model must be specified')
                if self.verbose_debug:
                    print('Model must be specified')
            raise ValueError('Model must be specified')

        self.query_config = db_query
        self.params_config = db_params
        self.params_config.parse_params(kwargs)

    def build_and_load(self):
        self.df = self._build_and_load()
        if self.df is not None:
            self._process_loaded_data()
        return self.df

    def _build_and_load(self) -> dd.DataFrame:
        query = self.connection_config.model.objects.using(self.connection_config.connection_name)
        if not self.params_config.filters:
            # IMPORTANT: if no filters are provided show only the first n_records
            # this is to prevent loading the entire table by mistake
            n_records = self.query_config.n_records if self.query_config.n_records else 100
            queryset=query.all()[:n_records]
        else:
            q_objects = self.__build_query_objects(self.params_config.filters, self.query_config.use_exclude)
            queryset = query.filter(q_objects)
        if queryset is not None:
            try:
                self.df = ReadFrameDask(queryset, **self.params_config.df_params).read_frame()
            except Exception as e:
                self.logger.critical(f'Error loading query: {str(queryset.query)}, error message: {e}')
                self.df = dd.from_pandas(pd.DataFrame(), npartitions=1)
        else:
            self.df = dd.from_pandas(pd.DataFrame(), npartitions=1)

        return self.df

    @staticmethod
    def __build_query_objects(filters: dict, use_exclude: bool):
        q_objects = Q()
        for key, value in filters.items():
            if not use_exclude:
                q_objects.add(Q(**{key: value}), Q.AND)
            else:
                q_objects.add(~Q(**{key: value}), Q.AND)
        return q_objects

    def _process_loaded_data(self):
        field_map = self.params_config.field_map
        if field_map is not None:
            rename_mapping = {k: v for k, v in field_map.items() if k in self.df.columns}
            if rename_mapping:
                # Apply renaming
                self.df = self.df.rename(columns=rename_mapping)
