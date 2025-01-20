"""
This module contains auxiliary functions that convert and assert int values.
"""

# DoITInt represents positive value between 0 and 5000
DoITInt = int

# UInt8 represents byte (0 to 255) value
UInt8 = int

# Maximum DoIT value
DOIT_INT_MAX = 5000

def assert_uint8(value: int):
    """Asserts uint8 value. Raises ValueError if assertion fails"""
    if not isinstance(value, int):
        raise ValueError(f"Invalid uint8 value: {value}")
    if value < 0 or value > 255:
        raise ValueError(f"Invalid uint8 value. Out of range: {value}")

def assert_doit_int(value: int):
    """Asserts DoIT int value. Raises ValueError if assertion fails"""
    if not isinstance(value, int):
        raise ValueError(f"Invalid DoIT int value: {value}")
    if value < 0 or value > DOIT_INT_MAX:
        raise ValueError(f"Invalid DoIT int value. Out of range: {value}")

def scale_by_uint8(value: int, scale: UInt8) -> UInt8:
    """Scales value by uint8 value"""
    assert_uint8(scale)
    return int(value * (scale / 255))

def doit_int_to_uint8(value: DoITInt):
    """Converts DoIT int value to uint8"""
    assert_doit_int(value)
    return int(255 * (value / DOIT_INT_MAX))

def uint8_to_doit_int(value: UInt8) -> DoITInt:
    """Converts uint8 value to DoIT int value"""
    assert_uint8(value)
    return int(value * (DOIT_INT_MAX / 255))
