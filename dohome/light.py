from json import dumps, loads
from .datagram import open_endpoint
from .constants import (
    API_PORT,
    CMD_GET_STATE,
    CMD_SET_STATE,
    CMD_GET_TIME,
    CMD_SET_POWER
)

class DoHomeLight():
    _sid = ''
    _addr = ''
    _conn = None

    def __init__(self, sid: str, addr: str):
        self._sid = sid
        self._addr = addr

    async def connect(self):
        """Create socket to light"""
        self._conn = await open_endpoint(
            self._addr,
            API_PORT
        )

    async def get_time(self):
        """Reads time from the device"""
        await self._send_command(
            self._format_command(CMD_GET_TIME)
        )

    async def get_color(self):
        """Reads color from the device"""
        return await self._send_command(
            self._format_command(CMD_GET_STATE)
        )

    async def turn_off(self):
        """Turns the device off"""
        return await self._send_command(
            self._format_command(CMD_SET_POWER, { "op": 0 })
        )

    async def set_rgb(self, r: int, g: int, b: int):
        """Sets RGB color to the device"""
        return await self._send_command(
            self._format_light_payload(
                self._dohome_from_byte(r),
                self._dohome_from_byte(g),
                self._dohome_from_byte(b),
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
            print(data)
            raise Exception('Command error')
        return data

    def _format_light_payload(self, r = 0, g = 0, b = 0, w = 0, m = 0):
        return self._format_command(CMD_SET_STATE, {
            'r': r,
            'g': g,
            'b': b,
            'w': w,
            'm': m
        })

    # pylint: disable-next=invalid-name
    def _format_command(self, cmd: int, payload = None) -> str:
        if payload is None:
            payload = {}
        payload["cmd"] = cmd
        return f"cmd=ctrl&devices={[{self._sid}]}&op={dumps(payload)}"

    def _byte_from_dohome(self, x: int):
        return int(255 * (x / 5000))
    
    def _dohome_from_byte(self, x: int):
        return int(5000 * (x / 255))
    