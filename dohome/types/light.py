"""Doit light types, model types, and conversions"""

from __future__ import annotations

import math
from enum import StrEnum
from typing import NotRequired, TypedDict, TypeGuard

from .common import DoDict
from .constants import DO_INT_MAX, KELVIN_DELTA, KELVIN_MAX, KELVIN_MIN
from .primitives import (
    DoBool,
    DoInt,
    UInt8,
    doint_to_uint8,
    is_doint,
    is_uint8,
    uint8_to_doint,
)

# DoWhite represents white temperature.
# Values should be 5000 in sum. Yellow first, blue second.
# For example if yellow is 2000 then blue should be 3000 to get 5000 total.
DoWhite = tuple[DoInt, DoInt]

# DoRGB represents 3 RGB color components (0–5000 each)
DoRGB = tuple[DoInt, DoInt, DoInt]


class DoLightState(TypedDict):
    """Represents the RGBW state of a light on the wire"""

    r: DoInt
    g: DoInt
    b: DoInt
    w: DoInt
    m: DoInt


def is_doit_light_state(x: DoDict) -> TypeGuard[DoLightState]:
    """Check if a dictionary is a valid Doit light state."""
    return (
        isinstance(x["r"], int)
        and is_doint(x["r"])
        and isinstance(x["g"], int)
        and is_doint(x["g"])
        and isinstance(x["b"], int)
        and is_doint(x["b"])
        and isinstance(x["w"], int)
        and is_doint(x["w"])
        and isinstance(x["m"], int)
        and is_doint(x["m"])
    )


class DoSetLightParams(DoLightState):
    """Parameters for setting the state of a light"""

    on: NotRequired[DoBool]


class DoSetEffectParams(TypedDict):
    """Parameters for setting an effect on a light"""

    index: int  # 1 – 27


# RGB represents a standard 0–255 RGB color
RGB = tuple[UInt8, UInt8, UInt8]


class LightMode(StrEnum):
    """Light mode"""

    RGB = "rgb"
    WHITE = "white"


class LightState(TypedDict):
    """User-friendly parsed light state"""

    is_on: bool
    brightness: UInt8
    mode: LightMode
    color: RGB
    temperature: int


def rgb_to_dorgb(color: RGB) -> DoRGB:
    """Converts standard RGB color to Doit RGB (0–5000)"""
    return tuple(map(uint8_to_doint, color))  # pyright: ignore[reportReturnType]


def dorgb_to_rgb(color: DoRGB) -> RGB:
    """Converts Doit RGB (0–5000) to standard RGB color"""
    return tuple(map(doint_to_uint8, color))  # pyright: ignore[reportReturnType]


def kelvin_to_dowhite(kelvin: int) -> DoWhite:
    """Converts kelvin temperature to Doit white value pair"""
    if not (KELVIN_MIN <= kelvin <= KELVIN_MAX):
        raise ValueError(f"Invalid kelvin value. Out of range: {kelvin}")

    percent = (kelvin - KELVIN_MIN) / KELVIN_DELTA
    yellow = int(percent * DO_INT_MAX)
    blue = DO_INT_MAX - yellow

    return (yellow, blue)


def _assert_doint(value: int):
    if not is_doint(value):
        raise ValueError(f"Invalid DoInt value. Out of range: {value}")


def dowhite_to_kelvin(value: DoWhite, brightness: int) -> int:
    """Converts Doit white value pair to kelvin temperature"""
    (yellow, blue) = value
    _assert_doint(yellow)
    _assert_doint(blue)
    _assert_doint(yellow + blue)

    yellow = (yellow / brightness) * 255
    percent = yellow / DO_INT_MAX
    return math.ceil(percent * KELVIN_DELTA) + KELVIN_MIN


def scale_by_uint8(value: int, scale: UInt8) -> int:
    """Scales int value by uint8 value"""
    return int(value * (scale / 255))


def apply_brightness(values: tuple[int, ...], scale: UInt8) -> tuple[int, ...]:
    """Scales all iterable values by uint8 brightness"""
    if scale == 255:
        return values

    if not is_uint8(scale):
        raise ValueError("scale must be a uint8 value")

    scaled_values = map(lambda x: scale_by_uint8(x, scale), values)
    return tuple(scaled_values)


def parse_doit_light_state(raw: DoDict) -> LightState:
    """Converts wire light state to user-friendly parsed state"""
    if not is_doit_light_state(raw):
        raise ValueError("Invalid light state")

    is_on = False
    mode = LightMode.WHITE
    brightness = 255
    temperature = 0

    rgb_color = dorgb_to_rgb((raw["r"], raw["g"], raw["b"]))
    white_total = sum([raw["w"], raw["m"]])

    if sum(rgb_color) > 0:
        mode = LightMode.RGB
        is_on = True
    elif white_total > 0:
        mode = LightMode.WHITE
        is_on = True
        brightness = doint_to_uint8(white_total)
        temperature = dowhite_to_kelvin((raw["w"], raw["m"]), brightness)

    return LightState(
        is_on=is_on,
        brightness=brightness,
        mode=mode,
        color=rgb_color,
        temperature=temperature,
    )
