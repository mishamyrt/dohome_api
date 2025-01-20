"""Persistent TCP client for writing short messages and reading responses"""
from typing import Optional
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class PersistentTCPStream:
    """Persistent TCP stream for writing short messages and reading responses"""
    _host: str
    _port: int
    _disconnect_timeout: float
    _request_timeout: float
    _disconnect_task = None
    _reader: Optional[asyncio.StreamReader] = None
    _writer: Optional[asyncio.StreamWriter] = None
    _lock = asyncio.Lock()

    def __init__(
            self,
            host: str,
            port: int,
            disconnect_timeout: float = 10.0,
            request_timeout: float = 2.0):
        self._host = host
        self._port = port
        self._disconnect_timeout = disconnect_timeout
        self._request_timeout = request_timeout

    @property
    def connected(self) -> bool:
        """Indicates whether the client is connected"""
        if self._writer is None:
            return False
        sock = self._writer.get_extra_info('socket')
        return sock is not None and sock.fileno() != -1

    async def disconnect(self, delay: float = 0.0):
        """Disconnects from the TCP device"""
        if not self.connected:
            _LOGGER.debug("Not connected to %s:%d", self._host, self._port)
            return
        if delay > 0.0:
            await asyncio.sleep(delay)
        _LOGGER.debug("Disconnecting from %s:%d", self._host, self._port)
        await self._lock.acquire()
        try:
            self._writer.close()
            await self._writer.wait_closed()
            self._disconnect_task.cancel()
            self._disconnect_task = None
        finally:
            self._lock.release()
        _LOGGER.debug("Disconnected from %s:%d", self._host, self._port)

    async def connect(self):
        """Connects to the TCP server"""
        if self.connected:
            _LOGGER.debug("Already connected to %s:%d", self._host, self._port)
            return
        await self._lock.acquire()
        try:
            _LOGGER.debug("Connecting to %s:%d", self._host, self._port)
            async with asyncio.timeout(1):
                self._reader, self._writer = await asyncio.open_connection(
                    self._host, self._port)
            _LOGGER.debug("Connected to %s:%d", self._host, self._port)
            self._keep_alive()
        finally:
            self._lock.release()

    def _keep_alive(self):
        if self._disconnect_task is not None:
            self._disconnect_task.cancel()
        self._disconnect_task = asyncio.create_task(
            self.disconnect(delay=self._disconnect_timeout))

    async def send(self, payload: bytes) -> bytes:
        """Sends request to TCP server"""
        if not self.connected:
            await self.connect()

        async with asyncio.timeout(self._request_timeout):
            self._writer.write(payload)
            await self._writer.drain()
            data = await self._reader.readline()
            self._keep_alive()
            return data
