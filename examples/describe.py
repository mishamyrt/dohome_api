"""DoHome api example"""

from asyncio import run
from dohome_api import discover_devices, open_device

DISCOVERY_HOST = "192.168.31.255"

async def main():
    """Example entrypoint"""
    print("Searching DoHome lights")
    devices = await discover_devices()
    if not devices:
        print("No devices found")
        return
    for dev in devices:
        device = open_device(dev['ip'])
        info = await device.get_info()
        state = await device.get_state()
        print(f"Device: {dev['ip']}")
        print(f"SID: {info['sid']}")
        print(f"MAC: {info['mac']}")
        print(f"Type: {info['type'].name}")
        print(f"Mode: {state['mode'].name}")

if __name__ == '__main__':
    run(main())
