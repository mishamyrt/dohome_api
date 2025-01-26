"""DoHome color brightness helpers tests"""
import pytest
from dohome.color.brightness import (
    scale_by_uint8,
    apply_brightness,
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
        apply_brightness((5000, 0), -1)
    with pytest.raises(ValueError):
        apply_brightness((5000, 0), 256)
