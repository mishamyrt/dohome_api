"""DoHome broadcast controll example"""

from asyncio import run
from json import dumps
from dohome_api import create_gateway

async def main():
    """Example entrypoint"""
    (gateway, _) = create_gateway("192.168.31.255")
    descriptions = await gateway.discover_devices()
    print(f"Discovered {len(descriptions)} devices")
    sids = list(map(lambda x: x["sid"], descriptions))
    print(f"SID: {dumps(sids)}")

if __name__ == '__main__':
    run(main())
