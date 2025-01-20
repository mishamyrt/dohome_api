"""DoHome connection exceptions"""

from .base import DoHomeException


class ConnectionException(DoHomeException):
    """Connection exception."""

class ConnectionTimeoutException(ConnectionException):
    """Connection timeout exception."""
    def __init__(self, host: str, port: int):
        super().__init__(f"Connection timeout: {host}:{port}")
