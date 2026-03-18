"""DoHome light control example: turn on, change color, turn off"""

import asyncio

from dohome.api import APIClient, discover
from dohome.transport import TCPStream, UDPBroadcast
from dohome.types.constants import KELVIN_MIN


async def main():
    broadcast = UDPBroadcast()
    devices = await discover(broadcast)
    _ = broadcast.close()

    if not devices:
        print("No devices found")
        return

    host = devices[0]["sta_ip"]
    print(f"Connecting to {host}")
    client = APIClient(TCPStream(host))

    print("Turning on")
    await client.set_power(True)
    await asyncio.sleep(2)

    print("Setting color to red at 50% brightness")
    await client.set_color((255, 0, 0), 128)
    await asyncio.sleep(2)

    print("Setting color to teal at full brightness")
    await client.set_color((0, 200, 180), 255)
    await asyncio.sleep(2)

    print("Setting warmest white at 80%")
    await client.set_white(KELVIN_MIN, 204)
    await asyncio.sleep(2)

    print("Turning off")
    await client.set_power(False)


if __name__ == "__main__":
    asyncio.run(main())
