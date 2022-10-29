"""DoHome light controller"""

from json import loads
from .datagram import open_endpoint
from .convert import (
    dohome_from_uint8,
    uint8_state_from_dohome,
    uint8_to_mireds
)
from .commands import (
    CMD_GET_STATE,
    CMD_GET_TIME,
    CMD_SET_POWER,
    format_command,
    format_light_payload
)
from .constants import (
    API_PORT,
)

class DoHomeLight():
    """DoHome light controller class"""
    _sid = ''
    _addr = ''
    _conn = None

    def __init__(self, sid: str, addr: str):
        self._sid = sid
        self._addr = addr

    @property
    def connected(self):
        """Indicates whether the socket is connected."""
        return self._conn is not None and not self._conn.closed

    async def connect(self):
        """Create socket to light"""
        if self.connected:
            self._conn.close()
        self._conn = await open_endpoint(
            self._addr,
            API_PORT
        )

    async def get_state(self) -> dict:
        """Reads high-level state from the device"""
        raw_state = await self.get_raw_state()
        uint8_state = uint8_state_from_dohome(raw_state)
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
            state["mireds"] = uint8_to_mireds(uint8_state["m"])
        return state

    async def get_raw_state(self):
        """Reads color from the device"""
        return await self._send_command(
            format_command(self._sid, CMD_GET_STATE)
        )

    async def get_time(self):
        """Reads time from the device"""
        await self._send_command(
            format_command(self._sid, CMD_GET_TIME)
        )

    async def set_enabled(self, enabled: bool):
        """Turns the device off"""
        return await self._send_command(
            format_command(self._sid, CMD_SET_POWER, { "op": 1 if enabled else 0 })
        )

    # pylint: disable-next=invalid-name
    async def set_rgb(self, r: int, g: int, b: int):
        """Sets RGB color to the device"""
        return await self._send_command(
            format_light_payload(
                self._sid,
                dohome_from_uint8(r),
                dohome_from_uint8(g),
                dohome_from_uint8(b),
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
    