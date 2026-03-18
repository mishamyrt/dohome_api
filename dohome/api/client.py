"""Doit API client"""

from __future__ import annotations

from datetime import datetime

from dohome.transport import APITransport
from dohome.types.common import DoDict
from dohome.types.constants import Command, Effect
from dohome.types.datetime import (
    encode_doit_datetime,
    parse_doit_datetime,
)
from dohome.types.device import (
    DeviceInfo,
    parse_doit_device_info,
)
from dohome.types.light import (
    RGB,
    DoSetEffectParams,
    DoSetLightParams,
    LightState,
    apply_brightness,
    kelvin_to_dowhite,
    parse_doit_light_state,
    rgb_to_dorgb,
)
from dohome.types.primitives import DoInt, UInt8
from dohome.types.wifi import (
    DoWiFiCredentials,
    is_doit_wifi_credentials_response,
)

from .message import assert_response, decode_message, format_command


class APIClient:
    """Doit API client"""

    _transport: APITransport

    def __init__(self, transport: APITransport):
        self._transport = transport

    async def reboot(self) -> None:
        """Reboots the device"""
        _ = await self._send_command(Command.REBOOT)

    async def get_device_info(self) -> DeviceInfo:
        """Returns device info"""
        resp = await self._send_command(Command.GET_DEVICE_INFO)
        return parse_doit_device_info(resp)

    async def get_datetime(self) -> datetime:
        """Reads datetime from the device"""
        resp = await self._send_command(Command.GET_TIME)
        return parse_doit_datetime(resp)

    async def set_datetime(self, dt: datetime) -> None:
        """Sets datetime to the device"""
        req = encode_doit_datetime(dt)
        _ = await self._send_command(Command.SET_TIME, req)

    async def get_wifi_credentials(self) -> DoWiFiCredentials:
        """Reads WiFi credentials from the device"""
        resp = await self._send_command(Command.WIFI_CREDENTIALS)
        if not is_doit_wifi_credentials_response(resp):
            raise ValueError("Invalid WiFi credentials response")
        return resp

    async def set_wifi_credentials(self, ssid: str, password: str) -> None:
        """Sets WiFi credentials to the device"""
        req: DoWiFiCredentials = {"ssid": ssid, "pass": password}
        _ = await self._send_command(Command.WIFI_CREDENTIALS, req)

    async def get_state(self) -> LightState:
        """Reads light state from the device"""
        resp = await self._send_command(Command.GET_STATE)
        return parse_doit_light_state(resp)

    async def set_power(self, is_on: bool) -> None:
        """Turns the device on or off"""
        await self._set_color_state(on=is_on)

    async def set_color(self, color: RGB, brightness: UInt8) -> None:
        """Sets RGB color to the device."""
        color = rgb_to_dorgb(color)
        [r, g, b] = apply_brightness(color, brightness)
        await self._set_color_state(r=r, g=g, b=b)

    async def set_white(self, kelvin: int, brightness: UInt8) -> None:
        """Sets white temperature to the device"""
        temp = kelvin_to_dowhite(kelvin)
        [w, m] = apply_brightness(temp, brightness)
        await self._set_color_state(w=w, m=m)

    async def set_effect(self, effect: Effect) -> None:
        """Sets effect to the device"""
        req: DoSetEffectParams = {"index": effect.value}
        _ = await self._send_command(Command.SET_EFFECT, req)

    async def _set_color_state(
        self,
        r: DoInt = 0,
        g: DoInt = 0,
        b: DoInt = 0,
        m: DoInt = 0,
        w: DoInt = 0,
        on: bool | None = None,
    ) -> None:
        params: DoSetLightParams = {"r": r, "g": g, "b": b, "m": m, "w": w}
        if on is not None:
            params["on"] = 1 if on else 0

        _ = await self._send_command(Command.SET_STATE, params)

    async def _send_command(self, cmd: Command, params: DoDict | None = None) -> DoDict:
        req = self._encode_request(cmd, params or {})
        res = await self._transport.send(req)
        return self._decode_response(res, cmd)

    def _encode_request(self, cmd: Command, params: DoDict) -> bytes:
        req = format_command(cmd, params) + "\r\n"
        return req.encode()

    def _decode_response(self, res: bytes, cmd: Command) -> DoDict:
        data = decode_message(res)
        return self._handle_response(data, cmd)

    def _handle_response(self, res: DoDict, cmd: Command) -> DoDict:
        assert_response(res, cmd)
        result: DoDict = {}
        for k, v in res.items():
            if k not in ["cmd", "res"]:
                result[k] = v
        return result
