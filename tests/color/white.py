"""DoHome white temperature helpers tests"""
import pytest
from dohome.color.white import (
    KELVIN_MAX,
    KELVIN_MIN,
    to_dowhite,
    from_dowhite,
)

def test_to_dowhite():
    """Test to_dowhite function"""
    assert to_dowhite(KELVIN_MAX) == (5000, 0)
    assert to_dowhite(KELVIN_MIN) == (0, 5000)
    assert to_dowhite(5000) == (2941, 2059)

    with pytest.raises(ValueError):
        to_dowhite(KELVIN_MAX + 1)
    with pytest.raises(ValueError):
        to_dowhite(KELVIN_MIN - 1)


def test_from_dowhite():
    """Test from_dowhite function"""
    assert from_dowhite((5000, 0), 255) == KELVIN_MAX
    assert from_dowhite((0, 5000), 255) == KELVIN_MIN
    assert from_dowhite((2941, 2059), 255) == 5000

    assert from_dowhite((1000, 0), 128) == 4355
    assert from_dowhite((0, 1000), 128) == 3000

    with pytest.raises(ValueError):
        from_dowhite((5001, 0), 255)
    with pytest.raises(ValueError):
        from_dowhite((0, 5001), 255)
    with pytest.raises(ValueError):
        from_dowhite((5000, 5000), 255)
    with pytest.raises(ValueError):
        from_dowhite((-1, 0), 255)
    with pytest.raises(ValueError):
        from_dowhite((0, -1), 255)
