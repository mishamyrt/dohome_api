"""DoHome api example"""

from asyncio import run
from dohome import DoHomeLight, discover_lights

SEARCH_TIMEOUT = 2
DISCOVERY_HOST = "192.168.31.255"

async def main():
    """Example entrypoint"""
    print(f"Searching DoHome lights for {SEARCH_TIMEOUT} seconds")
    descriptions = await discover_lights(DISCOVERY_HOST, SEARCH_TIMEOUT)
    for descr in descriptions:
        print(f"Connecting to {descr['sid']} on {descr['sta_ip']}")
        light = DoHomeLight(descr["sid"], descr["sta_ip"])
        await light.connect()
        state = await light.get_state()
        print(f"State: {state}")
    print(f"Done. Found {len(descriptions)} lights")

if __name__ == '__main__':
    run(main())
