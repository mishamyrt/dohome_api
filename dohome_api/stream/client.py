"""DoIT client"""
import asyncio

from dohome_api.exc import ConnectionTimeoutException
from dohome_api.doit import (
    PORT_TCP,
    MESSAGE_MAX_SIZE,
    Command,
    assert_response,
    format_command,
    parse_message
)

from .persistent import PersistentTCPStream

class DoITError(Exception):
    """DoIT client error"""

class StreamClient:
    """TCP DoIT client"""
    _stream: PersistentTCPStream

    def __init__(
            self,
            host: str,
            disconnect_timeout: float = 10.0,
            request_timeout: float = 2.0):
        self._stream = PersistentTCPStream(
            host, PORT_TCP, disconnect_timeout, request_timeout)

    @property
    def connected(self):
        """Indicates whether the client is connected"""
        return self._stream.connected

    async def disconnect(self):
        """Disconnects from the DoIT device"""
        await self._stream.disconnect()

    async def connect(self):
        """Connects to the DoIT server"""
        await self._stream.connect()

    async def send(self, cmd: Command, **kwargs) -> dict:
        """Sends request to DoIT device"""
        req_data = format_command(cmd, **kwargs) + "\n"

        if len(req_data) > MESSAGE_MAX_SIZE:
            raise DoITError("Message too long")

        try:
            res_data = await self._stream.send(req_data.encode())
            res = parse_message(res_data)
            assert_response(res, cmd)
            return res
        except asyncio.TimeoutError as exc:
            raise ConnectionTimeoutException from exc
