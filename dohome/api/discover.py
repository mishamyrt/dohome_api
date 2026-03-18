"""Doit API broadcast client"""

from dohome.transport import BroadcastAPITransport
from dohome.types.constants import DatagramCommand
from dohome.types.dgram import DoPingResponse, is_doit_ping_response

from .message import (
    decode_datagram,
    format_datagram,
)


async def discover(transport: BroadcastAPITransport) -> list[DoPingResponse]:
    """Discovers Doit API devices on the network"""
    req = format_datagram({"cmd": DatagramCommand.PING}) + "\n"
    res = await transport.send(req.encode())
    dgrams = map(decode_datagram, res)
    pongs: list[DoPingResponse] = []
    for dgram in dgrams:
        if not is_doit_ping_response(dgram):
            raise ValueError("Invalid datagram response", dgram)
        pongs.append(dgram)
    return pongs
