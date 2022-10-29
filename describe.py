"""DoHome api example"""

from asyncio import run
# from logging import basicConfig, DEBUG
from dohome import DoHomeLight, DoHomeGateway

# basicConfig(level=DEBUG)

DISCOVERY_HOST = "192.168.31.255"

async def main():
    """Example entrypoint"""
    print("Searching DoHome lights")
    gateway = DoHomeGateway(DISCOVERY_HOST)
    descriptions = await gateway.discover_lights()
    for descr in descriptions:
        print(f"Connecting to {descr['sid']} on {descr['sta_ip']}")
        light = DoHomeLight(descr["sid"], descr["sta_ip"])
        await light.connect()
        state = await light.get_state()
        await light.set_rgb(255, 0, 0, 100)
        print(f"State: {state}")
    print(f"Done. Found {len(descriptions)} lights")

if __name__ == '__main__':
    run(main())
