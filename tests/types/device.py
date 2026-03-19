"""Doit protocol parser tests"""

from dohome.types.device import DeviceType, parse_hardware_info


def test_parse_hardware_info():
    """Test parse_hardware_info function"""
    assert parse_hardware_info("286dcd767cac_DT-WYRGB_W600") == {
        "mac": "28:6d:cd:76:7c:ac",
        "sid": "7cac",
        "type": DeviceType.RGBW_BULB,
        "chip": "W600",
    }
    assert parse_hardware_info("4f4dcd766e00_STRIPE_ESP32") == {
        "mac": "4f:4d:cd:76:6e:00",
        "sid": "6e00",
        "type": DeviceType.LED_STRIP,
        "chip": "ESP32",
    }
