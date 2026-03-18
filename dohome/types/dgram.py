"""Doit datagram types"""

from typing import TypedDict, TypeGuard

from .common import DoDict


class DoPingResponse(TypedDict):
    """Response to a datagram ping request"""

    cmd: str
    host_ip: str
    sta_ip: str
    device_id: str
    device_key: str
    device_name: str
    device_type: str
    compandy_id: str  # Yes, it's a typo, but it's the field name in the protocol
    chip: str


def is_doit_ping_response(x: DoDict) -> TypeGuard[DoPingResponse]:
    """Check if a dictionary is a valid DoPingResponse"""
    return all(
        key in x and isinstance(x[key], str)
        for key in (
            "cmd",
            "host_ip",
            "sta_ip",
            "device_id",
            "device_key",
            "device_name",
            "device_type",
            "compandy_id",
            "chip",
        )
    )
