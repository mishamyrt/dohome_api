"""Doit client"""

import asyncio
from typing import override

from dohome.exc import ClientIsNotResponding, PayloadTooLong

from .base import APITransport
from .constants import MESSAGE_MAX_SIZE, PORT_TCP


class TCPStream(APITransport):
    """TCP stream Doit API transport"""

    _host: str
    _connect_timeout: float
    _request_timeout: float
    _resend_attempts: int

    def __init__(
        self,
        host: str,
        connect_timeout: float = 1.0,
        request_timeout: float = 3.5,
        resend_attempts: int = 3,
    ):
        self._host = host
        self._connect_timeout = connect_timeout
        self._request_timeout = request_timeout
        self._resend_attempts = resend_attempts

    @override
    async def send(self, payload: bytes) -> bytes:
        """Sends request to Doit device with retry logic"""
        attempts = self._resend_attempts
        while attempts > 0:
            try:
                return await self._try_send(payload)
            except asyncio.TimeoutError:
                attempts -= 1
        raise ClientIsNotResponding(self._host)

    async def _try_send(self, payload: bytes) -> bytes:
        if len(payload) > MESSAGE_MAX_SIZE:
            raise PayloadTooLong(len(payload))

        # Open TCP connection
        async with asyncio.timeout(self._connect_timeout):
            reader, writer = await asyncio.open_connection(self._host, PORT_TCP)
        # Send request
        writer.write(payload)
        try:
            async with asyncio.timeout(self._request_timeout):
                # Wait for response
                await writer.drain()
                data = await reader.read(MESSAGE_MAX_SIZE)
        finally:
            writer.close()
            await writer.wait_closed()
        return data
