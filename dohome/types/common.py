"""Doit API common types"""

from collections.abc import Mapping
from typing import TypedDict


class BaseRequest(TypedDict):
    """BaseRequest represents Doit protocol request"""

    cmd: int


class BaseResponse(TypedDict):
    """BaseResponse represents Doit protocol response"""

    cmd: int
    res: int


# Flat dict with supported types
DoDict = Mapping[str, object]
