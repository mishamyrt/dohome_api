"""DoHome color scale helpers"""
from __future__ import annotations
from typing import TypeVar
from dohome.api import DoRGB, DoWhite
from .int import assert_uint8, UInt8

def scale_by_uint8(value: int, scale: UInt8) -> UInt8:
    """Scales int value by uint8 value"""
    return int(value * (scale / 255))

T = TypeVar("T", DoRGB, DoWhite)

def apply_brightness(values: T, scale: UInt8) -> T:
    """Scales all iterable values by uint8 value"""
    if scale == 255:
        return values

    assert_uint8(scale)
    scaled_values = map(lambda x: scale_by_uint8(x, scale), values)
    return tuple(scaled_values)
