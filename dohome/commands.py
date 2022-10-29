"""DoHome protocol commands"""
from typing import (Final, List)
from json import (dumps, loads)

# Commands
CMD_SET_STATE: Final = 6
CMD_GET_STATE: Final = 25
CMD_SET_POWER: Final = 5
CMD_GET_TIME: Final = 9
CMD_GET_IP: Final = 19

# Requests
REQUEST_PING: Final = 'cmd=ping\r\n'

# pylint: disable-next=invalid-name, too-many-arguments
def format_light_request(sids: List[str], r = 0, g = 0, b = 0, w = 0, m = 0):
    """Formats DoHome light set command"""
    return format_request(sids, CMD_SET_STATE, {
        'r': r,
        'g': g,
        'b': b,
        'w': w,
        'm': m
    })

def format_request(sids: List[str], cmd: int, payload = None) -> str:
    """Formats DoHome command"""
    sids_strings = map(lambda x: f"'{x}'", sids)
    if payload is None:
        payload = {}
    payload["cmd"] = cmd
    return f"cmd=ctrl&devices=[{','.join(sids_strings)}]&op={dumps(payload)}"

def parse_response(data: str) -> dict:
    """Formats DoHome response"""
    parts = data.split('&')
    json_data = parts[len(parts) - 1].split('=')[1].strip()
    return loads(json_data)
