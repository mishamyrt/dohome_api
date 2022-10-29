"""DoHome protocol commands"""
from typing import Final
from json import dumps

# Commands
CMD_SET_STATE: Final = 6
CMD_GET_STATE: Final = 25
CMD_SET_POWER: Final = 5
CMD_GET_TIME: Final = 9
CMD_PING: Final = 'cmd=ping\r\n'.encode()

# pylint: disable-next=invalid-name
def format_light_payload(sid: str, r = 0, g = 0, b = 0, w = 0, m = 0):
    """Formats DoHome light set command"""
    return format_command(sid, CMD_SET_STATE, {
        'r': r,
        'g': g,
        'b': b,
        'w': w,
        'm': m
    })

def format_command(sid: str, cmd: int, payload = None) -> str:
    """Formats DoHome command"""
    if payload is None:
        payload = {}
    payload["cmd"] = cmd
    return f"cmd=ctrl&devices={[{sid}]}&op={dumps(payload)}"
