"""UDP Broadcast Transport"""

from __future__ import annotations

import asyncio
from collections import deque
from socket import AF_INET, SO_BROADCAST, SOCK_DGRAM, SOL_SOCKET, socket
from typing import override

from .base import BroadcastAPITransport
from .constants import PORT_UDP
from .utils import get_discovery_host

_Address = tuple[str, int]


class UDPBroadcast(BroadcastAPITransport):
    """UDP Broadcast Transport"""

    _address: _Address
    _read_timeout: float
    _sock: socket
    _queue: deque[bytes]
    _lock: asyncio.Lock
    _loop: asyncio.AbstractEventLoop
    _task: asyncio.Task[None]

    def __init__(
        self,
        host: str | None = None,
        read_timeout: float = 2.0,
        listen_port: int = 0,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        if host is None:
            host = get_discovery_host()
        self._address = (host, PORT_UDP)
        self._read_timeout = read_timeout

        self._sock = socket(AF_INET, SOCK_DGRAM)
        self._sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._sock.bind(("", listen_port))
        self._sock.setblocking(False)

        self._queue = deque()
        self._lock = asyncio.Lock()

        self._loop = loop or asyncio.get_event_loop()
        self._task = self._loop.create_task(self._listener())

    @override
    async def send(self, payload: bytes) -> list[bytes]:
        """Send a UDP broadcast payload and return the received messages"""
        _ = await self._loop.sock_sendto(
            self._sock,
            payload,
            self._address,
        )
        return await self.read(self._read_timeout)

    async def read(self, wait: float | None = None) -> list[bytes]:
        """Read messages from the UDP broadcast socket"""
        if wait is not None:
            await asyncio.sleep(wait)
        async with self._lock:
            messages = list(self._queue)
            self._queue.clear()
        return messages

    def close(self) -> bool:
        """
        Close the UDP broadcast socket

        If the broadcast is already closed, return `False`. Otherwise,
        closes the socket, cancels the task and returns `True`.
        """

        is_closed = self._task.cancel()
        if is_closed:
            self._sock.close()
        return is_closed

    async def _listener(self) -> None:
        """Listen for incoming UDP broadcasts"""
        while True:
            try:
                data, _ = await self._loop.sock_recvfrom(self._sock, 256)  # pyright: ignore[reportAny]
                async with self._lock:
                    self._queue.append(data)
            except asyncio.CancelledError:
                break
            except Exception as e:
                raise e
