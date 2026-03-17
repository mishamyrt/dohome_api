from asyncio import run
from os import environ

from dohome import APIClient, TCPStream


async def main():
    ssid = environ.get("DOHOME_SSID")
    password = environ.get("DOHOME_PASSWORD")
    if not ssid or not password:
        print("DOHOME_SSID and DOHOME_PASSWORD environment variables must be set")
        exit(1)

    stream = TCPStream("192.168.4.1")
    client = APIClient(stream)
    # Check connection
    try:
        await client.get_state()
    except Exception as e:
        print("Failed to connect to the device")
        print("Make sure your computer is connected to the device access point")
        exit(1)

    await client.set_wifi_credentials(ssid, password)
    print("WiFi credentials set successfully")


if __name__ == "__main__":
    run(main())
