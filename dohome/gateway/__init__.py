"""DoHome Gateway"""
from socket import getfqdn, gethostname, gethostbyname_ex
from ..constants import API_PORT
from ..datagram import open_broadcast
from ..commands import (
    REQUEST_PING
)
from .util import (apply_mask, parse_pong)

# 'cmd=ctrl&devices=[\'7b5b\']&op={"cmd":19}'
class DoHomeGateway:
    """DoHome gateway controller"""

    _host = ''
    _broadcast = None

    def __init__(self, host: str = None):
        self._host = host if host is not None else self._get_discovery_host()
        self._broadcast = None

    async def discover_lights(self, timeout=1.0):
        await self._connection()
        self._broadcast.send(REQUEST_PING)
        responses = await self._broadcast.receive(timeout)
        descriptions = []
        for response in responses:
            message = response.decode("utf-8")
            if message.startswith('cmd=pong'):
                descriptions.append(parse_pong(message))
        return descriptions

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
