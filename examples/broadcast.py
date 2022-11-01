"""DoHome broadcast controll example"""

from asyncio import run
from dohome_api import create_gateway, DoHomeLightsBroadcast

async def main():
    """Example entrypoint"""
    (gateway, broadcast) = create_gateway("192.168.31.255")
    descriptions = await gateway.discover_devices()
    print(f"Discovered {len(descriptions)} devices")
    sids = map(lambda x: x["sid"], descriptions)
    lights = DoHomeLightsBroadcast(list(sids), broadcast)
    print("Turning off all lights with broadcasted message")
    await lights.turn_off()

if __name__ == '__main__':
    run(main())
