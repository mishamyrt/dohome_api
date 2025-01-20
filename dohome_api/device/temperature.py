"""Temperature helpers"""

from dohome_api.int import DoITInt, DOIT_INT_MAX

KELVIN_MIN = 3000
KELVIN_MAX = 6400
_KELVIN_DELTA = KELVIN_MAX - KELVIN_MIN

def to_kelvin(value: DoITInt) -> int:
    """Converts DoIT value to kelvin"""
    assert 0 <= value <= DOIT_INT_MAX
    percent = value / DOIT_INT_MAX
    return int(percent * _KELVIN_DELTA) + KELVIN_MIN

def from_kelvin(kelvin: int) -> DoITInt:
    """Converts kelvin to DoIT value"""
    assert KELVIN_MIN <= kelvin <= KELVIN_MAX
    percent = (kelvin - KELVIN_MIN) / _KELVIN_DELTA
    return int(percent * DOIT_INT_MAX)
