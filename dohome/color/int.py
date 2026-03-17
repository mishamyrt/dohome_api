"""DoHome int helpers"""

from __future__ import annotations

import math

from dohome.api import DO_INT_MAX, DoInt

# UInt8 represents byte (0 to 255) value
UInt8 = int


def assert_uint8(value: int):
    """Asserts uint8 value"""
    if value < 0 or value > 255:
        raise ValueError(f"Invalid uint8 value. Out of range: {value}")


def assert_doint(value: int):
    """Asserts DoIT int value (0 to 5000)"""
    if value < 0 or value > DO_INT_MAX:
        raise ValueError(f"Invalid DoIT int value. Out of range: {value}")


def doint_to_uint8(value: DoInt):
    """Converts DoIT int value to uint8"""
    assert_doint(value)
    return math.ceil(255 * (value / DO_INT_MAX))


def uint8_to_doint(value: UInt8) -> DoInt:
    """Converts uint8 value to DoIT int value"""
    assert_uint8(value)
    return int(value * (DO_INT_MAX / 255))
