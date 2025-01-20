"""Describe handlers for the DoHome CLI"""

from typing import TypedDict
from arrrgs import command
from dohome_api.device import DoHomeDevice, LightState, LightMode
from dohome_api.doit import DeviceInfo

from .batch import get_devices, parallel_run


class DeviceDescription(TypedDict):
    """Device description"""
    info: DeviceInfo
    state: LightState

async def _get_description(device: DoHomeDevice) -> DeviceDescription:
    info = await device.get_info()
    state = await device.get_state()
    return {
        "info": info,
        "state": state,
    }

@command()
async def describe(args):
    """Describe the device(s)"""
    devices = await get_devices(args)
    descriptions = await parallel_run(_get_description, devices)
    for desc in descriptions:
        print(f"SID: {desc['info']['sid']}")
        print(f" - Mac: {desc['info']['mac']}")
        print(f" - Type: {desc['info']['type'].name}")
        print(f" - Mode: {desc['state']['mode'].name}")
        print(f" - Enabled: {desc['state']['is_on']}")
        print(f" - Brightness: {desc['state']['brightness']}")
        if desc['state']['mode'] == LightMode.RGB:
            print(f" - Color: {desc['state']['color']}")
        elif desc['state']['mode'] == LightMode.WHITE:
            print(f" - White temperature: {desc['state']['temperature']}")
