"""DoIT protocol constants"""

from enum import IntEnum, StrEnum

MESSAGE_MAX_SIZE = 256

PORT_UDP = 6091
PORT_TCP = 5555

class DeviceType(StrEnum):
    """DoHome device types"""
    RGBW_BULB = "DT-WYRGB"
    WHITE_BULB = "DT-WY"
    LED_STRIP = "STRIPE"

class Command(IntEnum):
    """DoIT protocol command codes"""
    SCAN_WIFI = 1
    MODIFY_SSID = 2 # {"cmd":2,"ssid":"abc","pass":"88888888"}
    REBOOT = 3
    GET_DEV_INFO = 4
    SWITCH_OPERATE = 5
    SET_STATE = 6 # {"cmd":6,"r":0,"g":1,"b":2,"w":3,"m":4,"on":1,"temp":1}
    SET_PRESET_MODE = 7 # {"cmd":7,"index":0,"freq":22}
    SET_CUSTOM_MODE = 8 # {"cmd":8,"colors":[{"r":1,"g":2,"b":3,"w":4},..],"mode":1,"freq":22}  # noqa: E501
    GET_TIME = 9
    ROUTER_CONFIG = 16 # ret {"cmd":16,"ssid":"test_ssid","pass":"12345567""..}
    GET_STATE = 25

class DatagramCommand(StrEnum):
    """DoIT protocol command codes"""
    PING = "ping"
    PONG = "pong"
    DOIT_COMMAND = "ctrl"

class ResponseCode(IntEnum):
    """DoIT protocol response codes"""
    OK = 0
    SCAN_FAILED = 1
    SCAN_TIMEOUT = 2
    INVALID_PASSWORD = 3
    GET_CMD_FAILED = 4
    GET_STATUS_FAILED = 5
    SCAN_RES_NULL = 6
    GET_PASSWORD_FAILED = 7
    GET_LED_OP_FAILED = 8
    GET_SSID_FAILED = 9
    GET_RED_FAILED = 10
    GET_BLUE_FAILED = 11
    GET_GREEN_FAILED = 12
    GET_WHITE_FAILED = 13
    GET_M_FAILED = 14
    GET_MODE_INDEX_FAILED = 15
    GET_FREQ_FAILED = 16
    GET_TIME_JSON_FAILED = 17
    GET_YEAR_FAILED = 18
    GET_MONTH_FAILED = 19
    GET_DAY_FAILED = 20
    GET_HOUR_FAILED = 21
    GET_MINUTE_FAILED = 22
    GET_SECOND_FAILED = 23
    MALLOC_FAILED = 24
    SET_SHUTDOWN_TIMER_FAILED = 25
    UNKNOWN_CMD = 26
    GET_TIMER_INDEX_FAILED = 27
    GET_DELAY_TIME_FAILED = 28
    GET_TYPE_FAILED = 29
    SET_TIMER_FAILED = 30
    GET_COLOR_ARR_FAILED = 31
    TOO_MANY_CUSTOM_COLOR = 32
    GET_OP_FAILED = 33
    CHANGE_RMT_CTRL_FAILED = 34
    GET_POWER_UP_INFO_FAILED = 35
    MODIFY_TIMER_FAILED = 36
    GET_MODE_LIST_FAILED = 37
    GET_MODE_ITEM_FAILED = 38
    GET_LOOP_FAILED = 39
    TOO_MANY_MODE = 40
    GET_REPEAT_FAILED = 41
    GET_TIMER_INFO_FAILED = 42
    GET_TIMEZONE_OFF_FAILED = 43
    NOT_CONN_ROUTER = 44
    GET_TIMESTAMP_FAILED = 45
    GET_REPEATER_EN_FAILED = 46
    GET_PORT_FAILED = 47
    GET_VAL_FAILED = 48
    GET_IS_ON_FAILED = 49
    GET_WEEKDAY_FAILED = 50
    GET_WRONG_WEEKDAY = 51
    GET_WEEKDAY_ITEM_FAILED = 52
    GET_ERROR_TIMER_TYPE = 53
    GET_ERROR_NO_PRODUCT = 54
