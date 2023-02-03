"""DoHome Gateway"""
from typing import Final, List, Union
from .commands import (
    CMD_GET_IP,
    format_request,
)
from .transport import DoHomeBroadcastTransport
from .light import DoHomeLightsBroadcast

REQUEST_PING: Final[str] = 'cmd=ping\r\n'

def parse_pong_sid(message: str) -> Union[str, None]:
    """Parses device sID from pong response"""
    records = list(map(lambda x: x.split('='), message.split('&')))
    for record in records:
        if record[0] == "device_name":
            name = record[1].strip()
            return name[len(name) - 4:]
    return None

class DoHomeGateway:
    """DoHome gateway controller"""

    _broadcast: DoHomeBroadcastTransport = None
    _timeout: float

    def __init__(self, gateway_ip = '255.255.255.255', timeout = 1.0):
        self._timeout = timeout
        self._broadcast = DoHomeBroadcastTransport(gateway_ip)

    def add_lights(self, sids: List[str]) -> DoHomeLightsBroadcast:
        """Creates new light by sid"""
        return DoHomeLightsBroadcast(sids, self._broadcast, self._timeout)

    async def discover_ip(self, sid: str) -> str:
        """Discovers DoHome light IP"""
        responses = await self._broadcast.send_request(
            format_request([sid], CMD_GET_IP)
        )
        if len(responses) != 1:
            raise Exception("Not found")
        parts = responses[0].decode("utf-8").split('"')
        return parts[len(parts) - 2]

    async def discover_devices(self, sends_count=3) -> List[str]:
        """Searches for DoHome devices on the network. Returns a list of sIDs"""
        sids = []
        while sends_count > 0:
            await self._broadcast.send_request(REQUEST_PING, receive=False)
            sends_count -= 1
        responses = await self._broadcast.receive()
        for response in responses:
            if response.startswith('cmd=pong'):
                sid = parse_pong_sid(response)
                if sid is not None and sid not in sids:
                    sids.append(sid)
        return sids
