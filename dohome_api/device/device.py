"""DoHome device module"""

from dohome_api.stream import StreamClient
from dohome_api.doit import DeviceInfo, Command, parse_device_info
from dohome_api.int import uint8_to_doit_int, scale_by_uint8, DOIT_INT_MAX

from .light_state import LightState, parse_state, RGBColor
from .temperature import from_kelvin

class DoHomeDevice:
    """DoHome device"""
    _client: StreamClient

    def __init__(self, client: StreamClient):
        self._client = client

    @property
    def connected(self):
        """
        Indicates whether the client is connected.
        To connect, just send any command"""
        return self._client.connected

    async def get_info(self) -> DeviceInfo:
        """Returns device info"""
        resp = await self._client.send(Command.GET_DEV_INFO)
        return parse_device_info(resp["dev_id"])

    async def reboot(self):
        """Reboots the device"""
        await self._client.send(Command.REBOOT)

    async def get_state(self) -> LightState:
        """Reads high-level state from the device"""
        resp = await self._client.send(Command.GET_STATE)
        return parse_state(resp)

    async def set_power(self, is_on: bool):
        """Turns the device on or off"""
        await self._client.send(
            Command.SET_STATE,
            on=1 if is_on else 0,
            # This is fields are ignored on power state update
            # but we need to send them anyway
            r=0, g=0, b=0, m=0, w=0)

    async def set_color(self, color: RGBColor, brightness = 255):
        """Sets RGB color to the device"""
        doit_colors = [0, 0, 0]
        for i in range(3):
            doit_colors[i] = scale_by_uint8(
                uint8_to_doit_int(color[i]),
                brightness)

        [r, g, b] = doit_colors
        await self._client.send(
            Command.SET_STATE,
            r=r,
            g=g,
            b=b,
            m=0,
            w=0)

    async def set_white_temperature(self, kelvin: int, brightness = 255):
        """Sets white temperature to the device"""
        white_value = from_kelvin(kelvin)
        blue_value = DOIT_INT_MAX - white_value

        white_value = scale_by_uint8(white_value, brightness)
        blue_value = scale_by_uint8(blue_value, brightness)
        await self._client.send(
            Command.SET_STATE,
            r=0,
            g=0,
            b=0,
            w=white_value,
            m=blue_value)

def open_device(host: str, **kwargs) -> DoHomeDevice:
    """Connects to the DoHome device"""
    return DoHomeDevice(StreamClient(host, **kwargs))
