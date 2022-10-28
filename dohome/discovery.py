"""DoHome discovery functions"""

from socket import getfqdn, gethostname, gethostbyname_ex
from typing import List
from .constants import API_PORT, CMD_PING
from .datagram import open_broadcast

def _apply_mask(local_address: str, mask: str) -> str:
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

def _get_discovery_host() -> str:
    hosts = gethostbyname_ex(getfqdn(gethostname()))
    local_ips = hosts[2]
    if len(local_ips) > 1:
        return ""
    return _apply_mask(local_ips[0], "255.255.255.0")

def _parse_pong(message: str) -> dict:
    records = list(map(lambda x: x.split('='), message.split('&')))
    descr = {
        record[0]: record[1].strip() for record in records
    }
    name = descr["device_name"]
    descr["sid"] = name[len(name) - 4:]
    return descr

async def discover_lights(host: str = None, timeout = 2.0) -> List[dict]:
    """Discovers DoHome lights on the network"""
    if host is None:
        host = _get_discovery_host()
    broadcast = await open_broadcast((host, API_PORT))
    broadcast.send(CMD_PING)
    responses = await broadcast.receive(timeout)
    descriptions = []
    for response in responses:
        message = response.decode("utf-8")
        if message.startswith('cmd=pong'):
            descriptions.append(_parse_pong(message))
    return descriptions
