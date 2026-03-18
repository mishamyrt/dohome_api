"""Doit device types, model types, and conversions"""

from typing import TypedDict, TypeGuard

from .common import DoDict
from .constants import DeviceType
from .primitives import DoBool, is_dobool


class DoDeviceInfo(TypedDict):
    """Device info as returned by the protocol"""

    tz: int
    ver: str
    dev_id: str
    conn: DoBool  # 0 - not connected, 1 - connected
    remote: DoBool  # 0 - remote control disabled, 1 - enabled
    save_off_stat: DoBool  # 0 - disabled, 1 - enabled
    repeater: DoBool  # 0 - disabled, 1 - enabled
    portal: DoBool  # 0 - disabled, 1 - enabled
    chip: str


class HardwareInfo(TypedDict):
    """Hardware info from device ID string."""

    mac: str
    sid: str
    chip: str
    type: DeviceType


class DeviceInfo(TypedDict):
    """Device info as returned by the protocol."""

    timezone: int
    version: str
    hardware: HardwareInfo


def is_doit_device_info(x: DoDict) -> TypeGuard[DoDeviceInfo]:
    """Check if a dictionary is a valid device info."""
    return (
        isinstance(x["tz"], int)
        and isinstance(x["ver"], str)
        and isinstance(x["dev_id"], str)
        and isinstance(x["conn"], int)
        and is_dobool(x["conn"])
        and isinstance(x["remote"], int)
        and is_dobool(x["remote"])
        and isinstance(x["save_off_stat"], int)
        and is_dobool(x["save_off_stat"])
        and isinstance(x["repeater"], int)
        and isinstance(x["portal"], int)
    )


def parse_doit_device_info(data: DoDict) -> DeviceInfo:
    """Parses a device info dictionary into a DeviceInfo object."""
    if not is_doit_device_info(data):
        raise ValueError("Invalid device info")
    return {
        "timezone": data["tz"],
        "version": data["ver"],
        "hardware": parse_hardware_info(data["dev_id"]),
    }


def format_mac_address(mac: str) -> str:
    """Formats a MAC address string."""
    return ":".join(mac[i : i + 2] for i in range(0, len(mac), 2))


def parse_hardware_info(device_id: str) -> HardwareInfo:
    """Extracts hardware info from device ID string"""
    mac = device_id[0:12]
    rest = device_id[13:]
    [device_type, chip] = rest.split("_")
    return {
        "mac": format_mac_address(mac),
        "sid": mac[-4:],
        "type": DeviceType(device_type),
        "chip": chip,
    }
