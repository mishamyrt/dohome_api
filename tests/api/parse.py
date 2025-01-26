"""DoIT protocol parser tests"""
from dohome.api import (
    DeviceType,
    decode_message,
    decode_datagram,
    parse_hardware_info,
)

def test_decode_message():
    """Test decode_message function"""
    assert decode_message(b'{"a":1,"b": 2}\n') == {"a": 1, "b": 2}
    assert decode_message(b'{"a":{"b":1,"c":"d"}}\n') == {"a": {"b": 1, "c": "d"}}

def test_decode_datagram():
    """Test decode_datagram function"""
    assert decode_datagram(b'a=[1,2,3]\r\n') == {"a": [1, 2, 3]}
    assert decode_datagram(b'a={"b":1,"c":"d"}\r\n') == {"a": {"b": 1, "c": "d"}}
    assert decode_datagram(b'a=1&b=2\r\n') == {"a": 1, "b": 2}

    assert decode_datagram(
        b'a={"b":1,"c": {"d":2}}&b=2&c=[1,2,3]\r\n') == {
            "a": {"b": 1, "c": {"d": 2}}, "b": 2, "c": [1, 2, 3]}

def test_parse_hardware_info():
    """Test parse_hardware_info function"""
    assert parse_hardware_info("286dcd767cac_DT-WYRGB_W600") == {
        "mac": "28:6d:cd:76:7c:ac",
        "sid": "7cac",
        "type": DeviceType.RGBW_BULB,
        "chip": "W600"
    }
    assert parse_hardware_info("4f4dcd766e00_STRIPE_ESP32") == {
        "mac": "4f:4d:cd:76:6e:00",
        "sid": "6e00",
        "type": DeviceType.LED_STRIP,
        "chip": "ESP32"
    }
