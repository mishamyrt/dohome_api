"""DoHome light control example: turn on, change color, turn off"""

import asyncio

from dohome import APIClient, TCPStream, UDPBroadcast, discover, to_dorgb, apply_brightness


async def main():
    broadcast = UDPBroadcast()
    devices = await discover(broadcast)
    broadcast.close()

    if not devices:
        print("No devices found")
        return

    host = devices[0]["sta_ip"]
    print(f"Connecting to {host}")
    client = APIClient(TCPStream(host))

    print("Turning on")
    await client.set_power(True)
    await asyncio.sleep(1)

    print("Setting color to red at 50% brightness")
    color = to_dorgb((255, 0, 0))
    color = apply_brightness(color, 128)
    await client.set_color(color)
    await asyncio.sleep(2)

    print("Setting color to teal at full brightness")
    color = to_dorgb((0, 200, 180))
    color = apply_brightness(color, 255)
    await client.set_color(color)
    await asyncio.sleep(2)

    print("Turning off")
    await client.set_power(False)


if __name__ == "__main__":
    asyncio.run(main())
