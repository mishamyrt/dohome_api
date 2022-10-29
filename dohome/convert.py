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

def apply_brightness(value: int, brightness_uint8: int) -> int:
    """Applies brightness to the value"""
    brightness_percent = brightness_uint8 / 255
    return int(value * brightness_percent)

class MiredsConverter:
    """Mireds to/from uint8 converter"""
    # pylint: disable=invalid-name
    _MIN = 0
    _MAX = 0
    _RANGE = 0

    def __init__(self, mireds_min: int, mireds_max: int):
        self._MIN = mireds_min
        self._MAX = mireds_max
        self._RANGE = mireds_max - mireds_min

    def to_uint8(self, mireds: int) -> int:
        """Converts mireds to uint8"""
        percent = (mireds - self._MIN) / self._RANGE
        return int(255 * percent)

    def to_mireds(self, uint8_temp: int) -> int:
        """Converts uint8 to mireds"""
        percent = uint8_temp / 255
        return int(percent * self._RANGE) + self._MIN
