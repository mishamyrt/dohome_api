"""DoHome color int helpers tests"""

import pytest

from dohome.types.primitives import (
    doint_to_uint8,
    is_doint,
    is_uint8,
    uint8_to_doint,
)


def test_is_uint8():
    """Test assert_uint8 function"""
    assert is_uint8(0)
    assert is_uint8(128)
    assert is_uint8(255)

    assert not is_uint8(-1)
    assert not is_uint8(256)


def test_is_doint():
    """Test is_doint function"""
    assert is_doint(0)
    assert is_doint(2510)
    assert is_doint(5000)

    assert not is_doint(-1)
    assert not is_doint(10000)


def test_doint_to_uint8():
    """Test doint_to_uint8 function"""
    assert doint_to_uint8(0) == 0
    assert doint_to_uint8(2509) == 128
    assert doint_to_uint8(5000) == 255

    with pytest.raises(ValueError):
        _ = doint_to_uint8(-1)
    with pytest.raises(ValueError):
        _ = doint_to_uint8(10000)


def test_uint8_to_doint():
    """Test uint8_to_doint function"""
    assert uint8_to_doint(0) == 0
    assert uint8_to_doint(255) == 5000
    assert uint8_to_doint(128) == 2509

    with pytest.raises(ValueError):
        _ = uint8_to_doint(-1)
    with pytest.raises(ValueError):
        _ = uint8_to_doint(256)
