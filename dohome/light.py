"""DoHome light controller"""

from json import loads
from typing import Final
from .datagram import open_endpoint
from .convert import (
    uint8_to_dohome,
    dohome_state_to_uint8,
    uint8_to_mireds
)
from .commands import (
    CMD_GET_STATE,
    CMD_GET_TIME,
    CMD_SET_POWER,
    format_request,
    format_light_request
)
from .constants import (
    API_PORT,
)

class DoHomeLight():
    """DoHome light controller class"""
    SID: Final = ''
    HOST = ''
    MIREDS_MIN: Final = 166
    MIREDS_MAX: Final = 400
    _conn = None

    def __init__(self, sid: str, host: str):
        # pylint: disable=invalid-name
        self.SID = sid
        self.HOST = host

    @property
    def connected(self):
        """Indicates whether the socket is connected."""
        return self._conn is not None and not self._conn.closed

    async def connect(self):
        """Create socket to light"""
        if self.connected:
            self._conn.close()
        self._conn = await open_endpoint(
            self.HOST,
            API_PORT
        )

    async def get_state(self) -> dict:
        """Reads high-level state from the device"""
        raw_state = await self.get_raw_state()
        uint8_state = dohome_state_to_uint8(raw_state)
        summ = 0
        state = {
            "enabled": False,
            "mode": "none", # none, rgb, white
            "rgb": [0, 0, 0],
            "mireds": 0
        }
        for color in ["r", "g", "b"]:
            summ += uint8_state[color]
        if summ > 0:
            state["enabled"] = True
            state["mode"] = "rgb"
            state["rgb"] = [
                uint8_state["r"], uint8_state["g"], uint8_state["b"]
            ]
            return state
        for temp in ["w", "m"]:
            summ += uint8_state[temp]
        if summ > 0:
            state["enabled"] = True
            state["mode"] = "white"
            state["mireds"] = uint8_to_mireds(uint8_state["m"], self.MIREDS_MIN, self.MIREDS_MAX)
        return state

    async def get_raw_state(self):
        """Reads color from the device"""
        return await self._send_command(
            format_request(self.SID, CMD_GET_STATE)
        )

    async def get_time(self):
        """Reads time from the device"""
        await self._send_command(
            format_request(self.SID, CMD_GET_TIME)
        )

    async def set_enabled(self, enabled: bool):
        """Turns the device off"""
        return await self._send_command(
            format_request(self.SID, CMD_SET_POWER, { "op": 1 if enabled else 0 })
        )

    # pylint: disable-next=invalid-name
    async def set_rgb(self, r: int, g: int, b: int):
        """Sets RGB color to the device"""
        return await self._send_command(
            format_light_request(
                self.SID,
                uint8_to_dohome(r),
                uint8_to_dohome(g),
                uint8_to_dohome(b),
            )
        )

    async def _send_command(self, request: str):
        self._conn.send(request.encode())
        response_data = await self._conn.receive()
        response = response_data.decode("utf-8")
        parts = response.split('&')
        json_data = parts[len(parts) - 1].split('=')[1].strip()
        data = loads(json_data)
        if data['res'] != 0:
            raise Exception('Command error')
        return data
    