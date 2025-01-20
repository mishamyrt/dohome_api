"""DoHome discovery utility functions"""
from socket import getfqdn, gethostname, gethostbyname_ex
from aiodatagram import open_broadcast
from .doit import (
    PORT_UDP,
    DatagramCommand,
    DeviceInfo,
    format_datagram_command,
    parse_datagram,
    parse_device_info,
)

class DiscoveredDeviceInfo(DeviceInfo):
    """DoIT discovered device info"""
    ip: str

def apply_mask(local_address: str, mask: str) -> str:
    """Applies the netmask to the /24 address"""
    segments = local_address.split(".")
    mask_segments = mask.split(".")
    result_address = ""
    index = 0
    for segment in mask_segments:
        if len(result_address) > 0:
            result_address += "."
        if segment == "255":
            result_address += f"{segments[index]}"
        elif segment == "0":
            result_address += "255"
        index += 1
    return result_address

def get_discovery_host() -> str:
    """Finds discovery host"""
    hosts = gethostbyname_ex(getfqdn(gethostname()))
    local_ips = hosts[2]
    if len(local_ips) > 1:
        return ""
    return apply_mask(local_ips[0], "255.255.255.0")

async def discover_devices(
        gateway: str = None,
        attempts: int=1,
        timeout: float=1) -> list[DiscoveredDeviceInfo]:
    """Searches for DoIT API devices on the network. Returns a list of sIDs"""
    if gateway is None:
        gateway = get_discovery_host()

    broadcast = await open_broadcast((gateway, PORT_UDP))
    payload = format_datagram_command(DatagramCommand.PING) + "\n"

    devices = []
    sids = set()

    while attempts >= 0:
        broadcast.send(payload.encode())
        responses = await broadcast.receive(timeout)
        for res, _ in responses:
            description = _parse_device_description(res)
            if description["sid"] not in sids:
                sids.add(description["sid"])
                devices.append(description)
        attempts -= 1

    broadcast.close()
    return devices

def _parse_device_description(res: bytes) -> DiscoveredDeviceInfo:
    message = parse_datagram(res)
    info = parse_device_info(message["device_id"])
    info["ip"] = message["sta_ip"]
    return info
