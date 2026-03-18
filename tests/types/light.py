"""DoHome light helpers tests"""

import pytest

from dohome.types.constants import KELVIN_MAX, KELVIN_MIN
from dohome.types.light import (
    LightMode,
    apply_brightness,
    dorgb_to_rgb,
    dowhite_to_kelvin,
    kelvin_to_dowhite,
    parse_doit_light_state,
    rgb_to_dorgb,
    scale_by_uint8,
)


def test_scale_by_uint8():
    """Test scale_by_uint8 function"""
    assert scale_by_uint8(0, 255) == 0
    assert scale_by_uint8(5000, 255) == 5000
    assert scale_by_uint8(5000, 128) == 2509
    assert scale_by_uint8(200, 100) == 78
    assert scale_by_uint8(200, 0) == 0


def test_apply_brightness():
    """Test apply_brightness function"""
    assert apply_brightness((0, 0, 0), 255) == (0, 0, 0)
    assert apply_brightness((255, 255, 0), 255) == (255, 255, 0)
    assert apply_brightness((255, 0, 255), 128) == (128, 0, 128)

    assert apply_brightness((5000, 0), 128) == (2509, 0)
    assert apply_brightness((5000, 0), 0) == (0, 0)

    with pytest.raises(ValueError):
        _ = apply_brightness((5000, 0), -1)
    with pytest.raises(ValueError):
        _ = apply_brightness((5000, 0), 256)


def test_parse_state():
    """Test parse_state function"""
    assert parse_doit_light_state({"r": 0, "g": 0, "b": 0, "w": 0, "m": 0}) == {
        "is_on": False,
        "brightness": 255,
        "mode": LightMode.WHITE,
        "color": (0, 0, 0),
        "temperature": 0,
    }

    assert parse_doit_light_state(
        {"r": 5000, "g": 2509, "b": 5000, "w": 0, "m": 0}
    ) == {
        "is_on": True,
        "brightness": 255,
        "mode": LightMode.RGB,
        "color": (255, 128, 255),
        "temperature": 0,
    }

    assert parse_doit_light_state({"r": 0, "g": 0, "b": 0, "w": 500, "m": 1500}) == {
        "is_on": True,
        "brightness": 102,
        "mode": LightMode.WHITE,
        "color": (0, 0, 0),
        "temperature": 3850,
    }


def test_rgb_to_dorgb():
    """Test to_dorgb function"""
    assert rgb_to_dorgb((0, 0, 0)) == (0, 0, 0)
    assert rgb_to_dorgb((255, 0, 0)) == (5000, 0, 0)
    assert rgb_to_dorgb((0, 255, 0)) == (0, 5000, 0)
    assert rgb_to_dorgb((0, 0, 255)) == (0, 0, 5000)
    assert rgb_to_dorgb((128, 128, 128)) == (2509, 2509, 2509)

    with pytest.raises(ValueError):
        _ = rgb_to_dorgb((256, 0, 0))
    with pytest.raises(ValueError):
        _ = rgb_to_dorgb((-1, 0, 0))


def test_dorgb_to_rgb():
    """Test from_dorgb function"""
    assert dorgb_to_rgb((0, 0, 0)) == (0, 0, 0)
    assert dorgb_to_rgb((5000, 0, 0)) == (255, 0, 0)
    assert dorgb_to_rgb((0, 5000, 0)) == (0, 255, 0)
    assert dorgb_to_rgb((0, 0, 5000)) == (0, 0, 255)
    assert dorgb_to_rgb((2509, 2509, 2509)) == (128, 128, 128)

    with pytest.raises(ValueError):
        _ = dorgb_to_rgb((5001, 0, 0))
    with pytest.raises(ValueError):
        _ = dorgb_to_rgb((-1, 0, 0))


def test_kelvin_to_dowhite():
    """Test to_dowhite function"""
    assert kelvin_to_dowhite(KELVIN_MAX) == (5000, 0)
    assert kelvin_to_dowhite(KELVIN_MIN) == (0, 5000)
    assert kelvin_to_dowhite(5000) == (2941, 2059)

    with pytest.raises(ValueError):
        _ = kelvin_to_dowhite(KELVIN_MAX + 1)
    with pytest.raises(ValueError):
        _ = kelvin_to_dowhite(KELVIN_MIN - 1)


def test_dowhite_to_kelvin():
    """Test from_dowhite function"""
    assert dowhite_to_kelvin((5000, 0), 255) == KELVIN_MAX
    assert dowhite_to_kelvin((0, 5000), 255) == KELVIN_MIN
    assert dowhite_to_kelvin((2941, 2059), 255) == 5000

    assert dowhite_to_kelvin((1000, 0), 128) == 4355
    assert dowhite_to_kelvin((0, 1000), 128) == 3000

    with pytest.raises(ValueError):
        _ = dowhite_to_kelvin((5001, 0), 255)
    with pytest.raises(ValueError):
        _ = dowhite_to_kelvin((0, 5001), 255)
    with pytest.raises(ValueError):
        _ = dowhite_to_kelvin((5000, 5000), 255)
    with pytest.raises(ValueError):
        _ = dowhite_to_kelvin((-1, 0), 255)
    with pytest.raises(ValueError):
        _ = dowhite_to_kelvin((0, -1), 255)
