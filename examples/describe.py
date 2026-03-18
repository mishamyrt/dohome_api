"""DoHome api example"""

from asyncio import run

from dohome.api import APIClient, discover
from dohome.transport import TCPStream, UDPBroadcast
from dohome.types.light import LightMode

DISCOVERY_HOST = "192.168.31.255"


async def main():
    """Example entrypoint"""
    broadcast = UDPBroadcast()
    devices = await discover(broadcast)
    _ = broadcast.close()
    if not devices:
        print("No devices found")
        return

    print(f"Found {len(devices)} devices")
    for device in devices:
        stream = TCPStream(device["sta_ip"])
        client = APIClient(stream)
        state = await client.get_state()
        print(f"- ID: {device['device_id']}")
        print(f"  Mode: {state['mode'].name}")
        print(f"  Enabled: {state['is_on']}")
        if not state["is_on"]:
            continue
        if state["mode"] == LightMode.RGB:
            print(f"  Color: {state['color']}")
        else:
            print(f"  Temperature: {state['temperature']}")
        print(f"  Brightness: {state['brightness']}")


if __name__ == "__main__":
    run(main())
