"""DoHome device discovery example"""

from asyncio import run
from dohome_api import discover_devices

async def main():
    """Example entrypoint"""
    devices = await discover_devices()
    if not devices:
        print("No devices found")
        return
    print(f"Found {len(devices)} devices")
    for device in devices:
        print(f"{device['ip']} {device['type'].name} {device['sid']}")

if __name__ == '__main__':
    run(main())
