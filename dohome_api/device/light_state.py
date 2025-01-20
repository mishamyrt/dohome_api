"""DoHome light state"""
from typing import TypedDict
from enum import Enum

from dohome_api.int import UInt8, doit_int_to_uint8

from .temperature import to_kelvin

RGBColor = tuple[UInt8, UInt8, UInt8]

class LightMode(Enum):
    """Light mode"""
    RGB = "rgb"
    WHITE = "white"

class LightState(TypedDict):
    """Light state"""
    is_on: bool
    brightness: UInt8
    mode: LightMode
    color: RGBColor
    temperature: int

def _parse_color(res: dict) -> RGBColor:
    rgb_color = map(doit_int_to_uint8, [res["r"], res["g"], res["b"]])
    return tuple(rgb_color)

def parse_state(res: dict) -> LightState:
    """Reads high-level state from the device"""

    is_on = False
    mode = LightMode.WHITE
    brightness = 255
    temperature = 0

    rgb_color = _parse_color(res)
    white_total = sum([res["w"], res["m"]])

    if sum(rgb_color) > 0:
        mode = LightMode.RGB
        is_on = True
    elif white_total > 0:
        mode = LightMode.WHITE
        is_on = True
        brightness = doit_int_to_uint8(white_total)
        temperature = to_kelvin(res["m"])

    return {
        "is_on": is_on,
        "brightness": brightness,
        "mode": mode,
        "color": rgb_color,
        "temperature": temperature
    }
