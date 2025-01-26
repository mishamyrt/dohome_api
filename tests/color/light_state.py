"""DoHome light state helpers tests"""
from dohome.color.light_state import parse_state, LightMode

def test_parse_state():
    """Test parse_state function"""
    assert parse_state({
        "r": 0,
        "g": 0,
        "b": 0,
        "w": 0,
        "m": 0
    }) == {
        "is_on": False,
        "brightness": 255,
        "mode": LightMode.WHITE,
        "color": (0, 0, 0),
        "temperature": 0
    }

    assert parse_state({
        "r": 5000,
        "g": 2509,
        "b": 5000,
        "w": 0,
        "m": 0
    }) == {
        "is_on": True,
        "brightness": 255,
        "mode": LightMode.RGB,
        "color": (255, 128, 255),
        "temperature": 0
    }

    assert parse_state({
        "r": 0,
        "g": 0,
        "b": 0,
        "w": 500,
        "m": 1500
    }) == {
        "is_on": True,
        "brightness": 102,
        "mode": LightMode.WHITE,
        "color": (0, 0, 0),
        "temperature": 3850,
    }
