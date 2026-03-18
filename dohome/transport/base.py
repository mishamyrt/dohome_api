"""Doit API transport"""

from abc import ABC, abstractmethod


class APITransport(ABC):
    """Doit API transport interface"""

    @abstractmethod
    async def send(self, payload: bytes) -> bytes:
        """Sends data to Doit API device"""


class BroadcastAPITransport(ABC):
    """Doit API broadcast transport interface"""

    @abstractmethod
    async def send(self, payload: bytes) -> list[bytes]:
        """Sends data to Doit API devices"""
