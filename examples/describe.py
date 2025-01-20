"""DoHome api example"""

from asyncio import run
from dohome_api import discover_devices, open_device

DISCOVERY_HOST = "192.168.31.255"

async def main():
    """Example entrypoint"""
    print("Searching DoHome lights")
    ips = await discover_devices()
    if not ips:
        print("No devices found")
        return
    for ip in ips:
        device = open_device(ip)
        info = await device.get_info()
        state = await device.get_state()
        print(f"Device: {ip}")
        print(f"SID: {info['sid']}")
        print(f"MAC: {info['mac']}")
        print(f"Type: {info['type'].name}")
        print(f"Mode: {state['mode'].name}")

if __name__ == '__main__':
    run(main())
