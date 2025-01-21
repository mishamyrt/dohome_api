"""DoIT client"""
import asyncio
from dohome_api.exc import PayloadTooLong, ClientIsNotResponding
from dohome_api.doit import (
    PORT_TCP,
    MESSAGE_MAX_SIZE,
    Command,
    assert_response,
    format_command,
    parse_message
)

class StreamClient:
    """TCP DoIT client"""
    _host: str
    _connect_timeout: float
    _request_timeout: float

    def __init__(
            self,
            host: str,
            connect_timeout: float = 1.0,
            request_timeout: float = 3.5):
        self._connect_timeout = connect_timeout
        self._request_timeout = request_timeout
        self._host = host

    async def _try_send(self, cmd: Command, **kwargs) -> dict:
        req_data = format_command(cmd, **kwargs) + "\r\n"

        if len(req_data) > MESSAGE_MAX_SIZE:
            raise PayloadTooLong(len(req_data))

        async with asyncio.timeout(self._connect_timeout):
            reader, writer = await asyncio.open_connection(
                self._host, PORT_TCP)

        writer.write(req_data.encode())
        try:
            async with asyncio.timeout(self._request_timeout):
                await writer.drain()
                data = await reader.readline()
        finally:
            writer.close()
            await writer.wait_closed()

        res = parse_message(data)
        assert_response(res, cmd)
        return res

    async def send(self, cmd: Command, attempts: int = 3, **kwargs) -> dict:
        """Sends request to DoIT device"""
        while attempts > 0:
            try:
                result = await self._try_send(cmd, **kwargs)
                return result
            except asyncio.TimeoutError:
                attempts -= 1
        raise ClientIsNotResponding(self._host)
