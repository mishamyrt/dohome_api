"""DoHome api example"""

from asyncio import run
from dohome_api import create_gateway, DoHomeLight

DISCOVERY_HOST = "192.168.31.255"

async def main():
    """Example entrypoint"""
    print("Searching DoHome lights")
    (gateway, _) = create_gateway(DISCOVERY_HOST)
    descriptions = await gateway.discover_devices()
    for descr in descriptions:
        print(f"Connecting to {descr['sid']} on {descr['sta_ip']}")
        light = DoHomeLight(descr["sid"], descr["sta_ip"])
        state = await light.get_state()
        print(f"State: {state}")
    print(f"Done. Found {len(descriptions)} lights")

if __name__ == '__main__':
    run(main())
