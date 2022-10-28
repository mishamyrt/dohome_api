"""Provide high-level UDP broadcast for asyncio"""

from asyncio import (
    DatagramProtocol,
    DatagramTransport,
    Queue,
    get_event_loop,
    sleep
)
from typing import (
    Tuple,
    Union,
    Text
)
from socket import (
    socket,
    SOL_SOCKET,
    SO_BROADCAST
)

Address = Tuple[str, int]

class Broadcast():
    """High-level UDP broadcaster"""
    def __init__(self):
        self._queue = Queue(0)
        self._closed = False
        self._transport = None
        self._write_ready_future = None

    def feed_datagram(self, data: bytes, addr: str):
        """Add response from datagram client"""
        self._queue.put_nowait((data, addr))

    def close(self):
        """Closes UDP broadcast"""
        if self._closed:
            return
        self._closed = True
        if self._queue.empty():
            self.feed_datagram(None, None)
        if self._transport:
            self._transport.close()

    def send(self, data):
        """Send a datagram to the given address."""
        if self._closed:
            raise IOError("Enpoint is closed")
        self._transport.sendto(data, None)

    async def receive(self, timeout=1.0):
        """Wait for an incoming datagram and return it with
        the corresponding address.
        This method is a coroutine.
        """
        await sleep(timeout)
        items = []
        if self._queue.empty() and self._closed:
            raise IOError("Enpoint is closed")
        while not self._closed:
            if self._queue.empty():
                return items
            item = await self._queue.get()
            items.append(item[0])
        return items

class BroadcastProtocol(DatagramProtocol):
    """Datagram broadcast protocol"""
    # pylint: disable=protected-access

    def __init__(self, broadcast: Broadcast):
        self._broadcast = broadcast
        self._transport = None

    def connection_made(self, transport: DatagramTransport):
        self._transport = transport
        sock = transport.get_extra_info("socket")  # type: socket.socket
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._broadcast._transport = transport

    def datagram_received(self, data: Union[bytes, Text], addr: Address):
        self._broadcast.feed_datagram(data, addr)

async def open_broadcast(addr: Address):
    """Creates datagram broadcast"""
    loop = get_event_loop()
    broadcast = Broadcast()
    await loop.create_datagram_endpoint(
        remote_addr=addr,
        protocol_factory=lambda: BroadcastProtocol(broadcast),
        allow_broadcast=True
    )
    return broadcast
