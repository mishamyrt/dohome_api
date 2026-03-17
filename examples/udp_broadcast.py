"""DoHome UDPBroadcast low-level usage example"""

import asyncio

from dohome import UDPBroadcast
from dohome.api.message import format_datagram, decode_datagram
from dohome.api.constants import DatagramCommand


async def main():
    broadcast = UDPBroadcast()

    ping = format_datagram({"cmd": DatagramCommand.PING}) + "\n"
    print(f"Sending ping: {ping.strip()}")

    responses = await broadcast.send(ping.encode())
    broadcast.close()

    if not responses:
        print("No responses received")
        return

    print(f"Received {len(responses)} response(s):")
    for raw in responses:
        datagram = decode_datagram(raw)
        print(f"  {datagram}")


if __name__ == "__main__":
    asyncio.run(main())
