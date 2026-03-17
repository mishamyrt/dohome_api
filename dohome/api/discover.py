"""DoIT API broadcast client"""

from logging import getLogger

from .constants import DatagramCommand
from .message import (
    decode_datagram,
    format_datagram,
)
from .transport import BroadcastAPITransport
from .types import (
    PingResponse,
)

_LOGGER = getLogger(__name__)


async def discover(transport: BroadcastAPITransport) -> list[PingResponse]:
    """Discovers DoIT API devices on the network"""
    req = format_datagram({"cmd": DatagramCommand.PING}) + "\n"
    res = await transport.send(req.encode())
    dgrams = map(decode_datagram, res)
    return list(dgrams)
