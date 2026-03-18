"""Doit datetime types"""

from datetime import datetime
from typing import TypedDict, TypeGuard

from .common import DoDict


class DoDatetime(TypedDict):
    """Doit protocol datetime representation"""

    year: int  # e.g. 2022
    mon: int  # e.g. 1
    day: int  # e.g. 27
    hour: int  # e.g. 15
    min: int  # e.g. 45
    sec: int  # e.g. 57


def is_doit_datetime(x: DoDict) -> TypeGuard[DoDatetime]:
    """Check if a dictionary is a valid Doit datetime."""
    return (
        isinstance(x["year"], int)
        and isinstance(x["mon"], int)
        and isinstance(x["day"], int)
        and isinstance(x["hour"], int)
        and isinstance(x["min"], int)
        and isinstance(x["sec"], int)
    )


def parse_doit_datetime(x: DoDict) -> datetime:
    """Parse a Doit datetime dictionary into a datetime object."""
    if not is_doit_datetime(x):
        raise ValueError("Invalid Doit datetime")
    return datetime(
        year=x["year"],
        month=x["mon"],
        day=x["day"],
        hour=x["hour"],
        minute=x["min"],
        second=x["sec"],
    )


def encode_doit_datetime(dt: datetime) -> DoDatetime:
    """Encode a datetime object into a Doit datetime dictionary."""
    return DoDatetime(
        year=dt.year,
        mon=dt.month,
        day=dt.day,
        hour=dt.hour,
        min=dt.minute,
        sec=dt.second,
    )
