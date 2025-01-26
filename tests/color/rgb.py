"""DoHome RGB color helpers tests"""
import pytest
from dohome.color.rgb import (
    to_dorgb,
    from_dorgb,
)


def test_to_dorgb():
    """Test to_dorgb function"""
    assert to_dorgb((0, 0, 0)) == (0, 0, 0)
    assert to_dorgb((255, 0, 0)) == (5000, 0, 0)
    assert to_dorgb((0, 255, 0)) == (0, 5000, 0)
    assert to_dorgb((0, 0, 255)) == (0, 0, 5000)
    assert to_dorgb((128, 128, 128)) == (2509, 2509, 2509)

    with pytest.raises(ValueError):
        to_dorgb((256, 0, 0))
    with pytest.raises(ValueError):
        to_dorgb((-1, 0, 0))

def test_from_dorgb():
    """Test from_dorgb function"""
    assert from_dorgb((0, 0, 0)) == (0, 0, 0)
    assert from_dorgb((5000, 0, 0)) == (255, 0, 0)
    assert from_dorgb((0, 5000, 0)) == (0, 255, 0)
    assert from_dorgb((0, 0, 5000)) == (0, 0, 255)
    assert from_dorgb((2509, 2509, 2509)) == (128, 128, 128)

    with pytest.raises(ValueError):
        from_dorgb((5001, 0, 0))
    with pytest.raises(ValueError):
        from_dorgb((-1, 0, 0))
