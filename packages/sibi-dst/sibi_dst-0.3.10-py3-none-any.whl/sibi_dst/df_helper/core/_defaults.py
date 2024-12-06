#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#
import json
from dataclasses import dataclass
from typing import Dict, Union, Optional

import pandas as pd

# This is the defaults configuration file for the df_helper module.

# conversion_map is a dictionary that maps the field types to their corresponding data type conversion functions.
# Each entry in the dictionary is a pair of a field type (as a string) and a callable function that performs the
# conversion. This mapping is used to convert the values in a pandas DataFrame to the appropriate data types based on
# the Django field type.

django_field_conversion_map: Dict[str, callable] = {
    "CharField": lambda x: x.astype(str),
    "TextField": lambda x: x.astype(str),
    "IntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "AutoField": lambda x: pd.to_numeric(x, errors="coerce"),
    "BigIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "SmallIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "PositiveIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "PositiveSmallIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "FloatField": lambda x: pd.to_numeric(x, errors="coerce"),
    "DecimalField": lambda x: pd.to_numeric(x, errors="coerce"),
    "BooleanField": lambda x: x.astype(bool),
    "NullBooleanField": lambda x: x.astype(bool),
    "DateTimeField": lambda x: pd.to_datetime(x, errors="coerce"),
    "DateField": lambda x: pd.to_datetime(x, errors="coerce").dt.date,
    "TimeField": lambda x: pd.to_datetime(x, errors="coerce").dt.time,
    "DurationField": lambda x: pd.to_timedelta(x, errors="coerce"),
    # for JSONField, assuming JSON objects are represented as string in df
    "JSONField": lambda x: x.apply(json.loads),
    "ArrayField": lambda x: x.apply(eval),
    "UUIDField": lambda x: x.astype(str),
}
