"""Doit protocol response assertion tests"""

import pytest

from dohome.api.message import (
    assert_response,
    decode_datagram,
    decode_message,
    format_command,
    format_datagram,
    format_datagram_command,
)
from dohome.exc import (
    CommandCodeInvalid,
    CommandCodeNotFound,
    ResponseCodeInvalid,
    ResponseCodeNotFound,
)
from dohome.types.constants import Command, DatagramCommand, ResponseCode


def test_assert_response():
    """Test assert_response function"""
    with pytest.raises(CommandCodeNotFound):
        assert_response({"a": 1, "b": 2}, Command.GET_TIME)
    with pytest.raises(CommandCodeInvalid):
        assert_response({"cmd": Command.GET_STATE.value, "b": 2}, Command.GET_TIME)
    with pytest.raises(ResponseCodeNotFound):
        assert_response({"cmd": Command.GET_TIME.value}, Command.GET_TIME)
    with pytest.raises(ResponseCodeInvalid):
        assert_response({"cmd": Command.GET_TIME.value, "res": 1}, Command.GET_TIME)

    assert_response(
        {"cmd": Command.GET_TIME.value, "res": ResponseCode.OK.value}, Command.GET_TIME
    )


def test_format_command():
    """Test format_command function"""
    assert format_command(Command.GET_DEVICE_INFO) == '{"cmd":4}'
    assert (
        format_command(Command.SET_STATE, {"r": 1, "g": 2, "b": 3, "m": 4, "w": 5})
        == '{"cmd":6,"r":1,"g":2,"b":3,"m":4,"w":5}'
    )  # noqa: E501


def test_format_datagram():
    """Test format_datagram function"""
    assert format_datagram({"a": 1, "b": 2}) == "a=1&b=2"
    assert format_datagram({"a": [1, 2, 3]}) == "a=[1,2,3]"
    assert format_datagram({"a": {"b": 1, "c": 2}}) == 'a={"b":1,"c":2}'


def test_format_datagram_command():
    """Test format_datagram_command function"""
    assert format_datagram_command(DatagramCommand.PING, {}) == "cmd=ping"
    assert (
        format_datagram_command(
            DatagramCommand.CTRL,
            {"op": {"cmd": Command.SET_STATE, "r": 1, "g": 2, "b": 3, "m": 4, "w": 5}},
        )
        == 'cmd=ctrl&op={"cmd":6,"r":1,"g":2,"b":3,"m":4,"w":5}'
    )


def test_decode_message():
    """Test decode_message function"""
    assert decode_message(b'{"a":1,"b": 2}\n') == {"a": 1, "b": 2}
    assert decode_message(b'{"a":{"b":1,"c":"d"}}\n') == {"a": {"b": 1, "c": "d"}}


def test_decode_datagram():
    """Test decode_datagram function"""
    assert decode_datagram(b"a=[1,2,3]\r\n") == {"a": [1, 2, 3]}
    assert decode_datagram(b'a={"b":1,"c":"d"}\r\n') == {"a": {"b": 1, "c": "d"}}
    assert decode_datagram(b"a=1&b=2\r\n") == {"a": 1, "b": 2}

    assert decode_datagram(b'a={"b":1,"c": {"d":2}}&b=2&c=[1,2,3]\r\n') == {
        "a": {"b": 1, "c": {"d": 2}},
        "b": 2,
        "c": [1, 2, 3],
    }
