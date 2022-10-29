"""
The DoHome bulb protocol from DoIT uses a 0 to 5000 measurement system.
It contains auxiliary functions that convert these values.
Also contains converters for temperature.
"""

MIREDS_MIN = 166
MIREDS_MAX = 400

def uint8_from_dohome(value: int):
    """Converts DoHome value to uint8"""
    return int(255 * (value / 5000))

def dohome_from_uint8(value: int):
    """Converts uint8 value to DoHome"""
    return int(5000 * (value / 255))

def uint8_state_from_dohome(raw_state: dict) -> dict:
    """Converts all values of dict from dohome to uint8"""
    for key in raw_state:
        raw_state[key] = uint8_from_dohome(raw_state[key])
    return raw_state

def mireds_to_uint8(mireds: int) -> int:
    ranged_temp = mireds - MIREDS_MIN
    percent = ranged_temp / MIREDS_MAX
    return int(255 * percent)

def uint8_to_mireds(byte_temp: int) -> int:
    percent = byte_temp / 255
    return int(percent *  MIREDS_MAX) + MIREDS_MIN
