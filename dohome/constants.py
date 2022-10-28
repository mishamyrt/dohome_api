"""DoHome contantants"""
from typing import Final

# Commands
CMD_SET_STATE: Final = 6
CMD_GET_STATE: Final = 25
CMD_SET_POWER: Final = 5
CMD_GET_TIME: Final = 9
CMD_PING: Final = 'cmd=ping\r\n'.encode()

# Connection
API_PORT: Final = 6091
BUFFER_SIZE: Final = 1024
