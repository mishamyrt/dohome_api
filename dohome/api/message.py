"""Doit protocol operation formatter"""

from __future__ import annotations

import json
from enum import Enum

from dohome.exc import (
    CommandCodeInvalid,
    CommandCodeNotFound,
    ResponseCodeInvalid,
    ResponseCodeNotFound,
)
from dohome.types.common import DoDict
from dohome.types.constants import Command, DatagramCommand, ResponseCode


def _dump_minified_json(data: dict[str, object] | list[int | str]) -> str:
    """Formats minified JSON string"""
    return json.dumps(data, separators=(",", ":"))


def format_command(cmd: Command, params: DoDict | None = None) -> str:
    """Formats Doit command request"""
    req: dict[str, object] = {
        "cmd": cmd.value,
    }
    if params is not None:
        for key, value in params.items():
            req[key] = value
    return _dump_minified_json(req)


def decode_message(res: bytes) -> DoDict:
    """Decodes Doit response"""
    data = res.decode("utf-8")
    return json.loads(data)  # pyright: ignore[reportAny]


def assert_response(res: DoDict, cmd: Command):
    """Asserts Doit response"""
    if "cmd" not in res:
        raise CommandCodeNotFound(res, cmd.value, cmd.name)
    res_cmd = Command(res["cmd"])
    if res_cmd != cmd:
        raise CommandCodeInvalid(res_cmd.value, cmd.value, cmd.name)
    if "res" not in res:
        raise ResponseCodeNotFound(res)
    res_code = ResponseCode(res["res"])
    if res_code != ResponseCode.OK:
        raise ResponseCodeInvalid(res_code.value, res_code.name)


def format_datagram(req: DoDict) -> str:
    """Formats Doit datagram request"""
    params: list[str] = []
    for key, value in req.items():  # pyright: ignore[reportAssignmentType]
        if isinstance(value, list | dict):
            value = _dump_minified_json(value)
        elif isinstance(value, Enum):
            value: int | str = value.value  # pyright: ignore[reportAny]
        params.append(f"{key}={value}")
    datagram = "&".join(params)
    return datagram


def format_datagram_command(cmd: DatagramCommand, params: DoDict) -> str:
    """Formats Doit datagram command request"""
    req: DoDict = {
        "cmd": cmd.value,
    }
    for key, value in params.items():
        req[key] = value  # pyright: ignore[reportArgumentType]
    return format_datagram(req)


def decode_datagram(res: bytes) -> DoDict:
    """Decodes Doit datagram response"""
    data = res.decode("utf-8").strip()
    entries = map(lambda x: x.split("="), data.split("&"))
    res_dict: DoDict = dict(entries)
    result: DoDict = {}
    for key, value in res_dict.items():
        if value.startswith("{") or value.startswith("["):
            result[key] = json.loads(value)
        elif value.isdigit():
            result[key] = int(value)
        else:
            result[key] = value
    return result
