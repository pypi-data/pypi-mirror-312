import datetime
from typing import Union, Tuple, Callable, Dict, Any
import pandas as pd
from sibi_dst.utils import Logger


class DateUtils:
    _PERIOD_FUNCTIONS: Dict[str, Callable[[], Tuple[datetime.date, datetime.date]]] = {}

    def __init__(self, logger=None):
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    @classmethod
    def _ensure_date(cls, value: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Ensure the input is converted to a datetime.date object.
        """
        if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, pd.Timestamp):
            return value.to_pydatetime().date()
        elif isinstance(value, str):
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    return datetime.datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Unsupported date format: {value}")

    @classmethod
    def calc_week_range(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> Tuple[datetime.date, datetime.date]:
        """
        Calculate the start and end of the week for a given reference date.
        """
        reference_date = cls._ensure_date(reference_date)
        start = reference_date - datetime.timedelta(days=reference_date.weekday())
        end = start + datetime.timedelta(days=6)
        return start, end

    @staticmethod
    def get_year_timerange(year: int) -> Tuple[datetime.date, datetime.date]:
        """
        Get the start and end dates for a given year.
        """
        return datetime.date(year, 1, 1), datetime.date(year, 12, 31)

    @classmethod
    def get_first_day_of_the_quarter(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Get the first day of the quarter for a given date.
        """
        reference_date = cls._ensure_date(reference_date)
        quarter = (reference_date.month - 1) // 3 + 1
        return datetime.date(reference_date.year, 3 * quarter - 2, 1)

    @classmethod
    def get_last_day_of_the_quarter(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Get the last day of the quarter for a given date.
        """
        reference_date = cls._ensure_date(reference_date)
        quarter = (reference_date.month - 1) // 3 + 1
        first_day_of_next_quarter = datetime.date(reference_date.year, 3 * quarter + 1, 1)
        return first_day_of_next_quarter - datetime.timedelta(days=1)

    @classmethod
    def get_month_range(cls, n: int = 0) -> Tuple[datetime.date, datetime.date]:
        """
        Get the date range for the current month or the month `n` months in the past or future.
        """
        today = datetime.date.today()
        target_month = (today.month - 1 + n) % 12 + 1
        target_year = today.year + (today.month - 1 + n) // 12
        start = datetime.date(target_year, target_month, 1)
        if n == 0:
            return start, today
        next_month = (target_month % 12) + 1
        next_year = target_year + (target_month == 12)
        end = datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)
        return start, end

    @classmethod
    def register_period(cls, name: str, func: Callable[[], Tuple[datetime.date, datetime.date]]):
        """
        Dynamically register a new period function.
        """
        cls._PERIOD_FUNCTIONS[name] = func

    @classmethod
    def parse_period(cls, **kwargs) -> Tuple[datetime.date, datetime.date]:
        """
        Parse the period keyword to determine the start and end date for date range operations.
        """
        period = kwargs.setdefault('period', 'today')
        period_functions = cls._get_default_periods()
        period_functions.update(cls._PERIOD_FUNCTIONS)
        if period not in period_functions:
            raise ValueError(f"Unknown period '{period}'. Available periods: {list(period_functions.keys())}")
        return period_functions[period]()

    @classmethod
    def _get_default_periods(cls) -> Dict[str, Callable[[], Tuple[datetime.date, datetime.date]]]:
        """
        Get default period functions.
        """
        today = datetime.date.today
        return {
            'today': lambda: (today(), today()),
            'yesterday': lambda: (today() - datetime.timedelta(days=1), today() - datetime.timedelta(days=1)),
            'current_week': lambda: cls.calc_week_range(today()),
            'last_week': lambda: cls.calc_week_range(today() - datetime.timedelta(days=7)),
            'current_month': lambda: cls.get_month_range(n=0),
            'last_month': lambda: cls.get_month_range(n=-1),
            'current_year': lambda: cls.get_year_timerange(today().year),
            'current_quarter': lambda: (cls.get_first_day_of_the_quarter(today()), cls.get_last_day_of_the_quarter(today())),
            'ytd': lambda: (datetime.date(today().year, 1, 1), today()),
        }

# Class enhancements
# DateUtils.register_period('next_week', lambda: (datetime.date.today() + datetime.timedelta(days=7),
#                                                 datetime.date.today() + datetime.timedelta(days=13)))
# start, end = DateUtils.parse_period(period='next_week')
# print(f"Next Week: {start} to {end}")
