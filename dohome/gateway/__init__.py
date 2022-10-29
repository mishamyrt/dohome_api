"""DoHome Gateway"""
from socket import getfqdn, gethostname, gethostbyname_ex
from ..constants import API_PORT
from ..datagram import open_broadcast
from ..light import DoHomeLight
from ..commands import (
    REQUEST_PING,
    CMD_GET_IP,
    format_request,
    parse_response
)
from .util import (apply_mask, parse_pong)

class DoHomeGateway:
    """DoHome gateway controller"""

    _host = ''
    _broadcast = None

    def __init__(self, host: str = None):
        self._host = host if host is not None else self._get_discovery_host()
        self._broadcast = None

    async def add_light(self, sid: str) -> DoHomeLight:
        host = await self.discover_ip(sid)
        print(host)
        return DoHomeLight(sid, host)

    async def discover_ip(self, sid: str) -> str:
        """Discovers DoHome light IP"""
        await self._connection()
        responses = await self._request(
            format_request([sid], CMD_GET_IP)
        )
        if len(responses) != 1:
            raise IOError
        parts = responses[0].decode("utf-8").split('"')
        return parts[len(parts) - 2]

    async def discover_lights(self, timeout=1.0):
        """Discovers DoHome lights"""
        await self._connection()
        responses = await self._request(REQUEST_PING, timeout)
        descriptions = []
        for response in responses:
            message = response.decode("utf-8")
            if message.startswith('cmd=pong'):
                descriptions.append(parse_pong(message))
        return descriptions

    async def _request(self, req: str, timeout=0.2) -> list:
        self._broadcast.send(req.encode())
        return await self._broadcast.receive(timeout)

    async def _connection(self):
        if self._broadcast is None or self._broadcast.closed:
            await self._connect()

    async def _connect(self):
        self._broadcast = await open_broadcast((self._host, API_PORT))

    def _get_discovery_host(self) -> str:
        hosts = gethostbyname_ex(getfqdn(gethostname()))
        local_ips = hosts[2]
        if len(local_ips) > 1:
            return ""
        return apply_mask(local_ips[0], "255.255.255.0")
