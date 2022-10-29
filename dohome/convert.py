"""
The DoHome bulb protocol from DoIT uses a 0 to 5000 measurement system.
It contains auxiliary functions that convert these values.
Also contains converters for temperature.
"""

def dohome_to_uint8(value: int):
    """Converts DoHome value to uint8"""
    return int(255 * (value / 5000))

def uint8_to_dohome(value: int):
    """Converts uint8 value to DoHome"""
    return int(5000 * (value / 255))

def dohome_state_to_uint8(raw_state: dict) -> dict:
    """Converts all values of dict from dohome to uint8"""
    for key in raw_state:
        raw_state[key] = dohome_to_uint8(raw_state[key])
    return raw_state

def mireds_to_uint8(mireds: int, mireds_min: int, mireds_max: int) -> int:
    """Converts mireds to uint8"""
    ranged_temp = mireds - mireds_min
    percent = ranged_temp / mireds_max
    return int(255 * percent)

def uint8_to_mireds(byte_temp: int, mireds_min: int, mireds_max: int) -> int:
    """Converts uint8 to mireds"""
    percent = byte_temp / 255
    return int(percent *  mireds_max) + mireds_min
