import pytest
from dohome_api.int import (
    assert_uint8,
    assert_doit_int,
    doit_int_to_uint8,
    uint8_to_doit_int,
    scale_by_uint8,
)


def test_assert_uint8():
    """Test assert_uint8 function"""
    assert_uint8(0)
    assert_uint8(128)
    assert_uint8(255)

    with pytest.raises(ValueError):
        assert_uint8(-1)
    with pytest.raises(ValueError):
        assert_uint8(256)
    with pytest.raises(ValueError):
        assert_uint8(1.2)
    with pytest.raises(ValueError):
        assert_uint8("1")

def test_assert_doit_int():
    """Test assert_doit_int function"""
    assert_doit_int(0)
    assert_doit_int(5000)
    assert_doit_int(2510)

    with pytest.raises(ValueError):
        assert_doit_int(-1)
    with pytest.raises(ValueError):
        assert_doit_int(10000)
    with pytest.raises(ValueError):
        assert_doit_int(1.2)
    with pytest.raises(ValueError):
        assert_doit_int("1")

def test_doit_int_to_uint8():
    """Test doit_int_to_uint8 function"""
    assert doit_int_to_uint8(0) == 0
    assert doit_int_to_uint8(5000) == 255
    assert doit_int_to_uint8(2510) == 128

    with pytest.raises(ValueError):
        doit_int_to_uint8(-1)

def test_uint8_to_doit_int():
    """Test uint8_to_doit_int function"""
    assert uint8_to_doit_int(0) == 0
    assert uint8_to_doit_int(255) == 5000
    assert uint8_to_doit_int(128) == 2509

    with pytest.raises(ValueError):
        uint8_to_doit_int(-1)

def test_scale_by_uint8():
    """Test scale_by_uint8 function"""
    assert scale_by_uint8(0, 255) == 0
    assert scale_by_uint8(5000, 255) == 5000
    assert scale_by_uint8(5000, 128) == 2509
    assert scale_by_uint8(200, 100) == 78

    with pytest.raises(ValueError):
        scale_by_uint8(200, -1)
