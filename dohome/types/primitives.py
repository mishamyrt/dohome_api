"""Doit protocol primitive types and conversions"""

import math
from typing import Literal, TypeGuard

from .constants import DO_INT_MAX

# DoInt represents positive value between 0 and 5000
DoInt = int

# UInt8 represents byte (0 to 255) value
UInt8 = int

# DoBool represents boolean value. 0 is False, 1 is True.
DoBool = Literal[0, 1]


def is_uint8(value: int) -> TypeGuard[UInt8]:
    """Asserts uint8 value"""
    return 0 <= value <= 255


def is_doint(value: int) -> TypeGuard[DoInt]:
    """Asserts Doit int value (0 to 5000)"""
    return 0 <= value <= DO_INT_MAX


def is_dobool(value: int) -> TypeGuard[DoBool]:
    """Asserts DoBool value (0 or 1)"""
    return value in (0, 1)


def doint_to_uint8(value: DoInt) -> UInt8:
    """Converts Doit int value to uint8"""
    if not is_doint(value):
        raise ValueError(f"Invalid DoInt value: {value}")
    return math.ceil(255 * (value / DO_INT_MAX))


def uint8_to_doint(value: UInt8) -> DoInt:
    """Converts uint8 value to Doit int value"""
    if not is_uint8(value):
        raise ValueError(f"Invalid UInt8 value: {value}")
    return int(value * (DO_INT_MAX / 255))
