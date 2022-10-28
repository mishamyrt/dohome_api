"""DoHome light discovery example"""

# pylint: disable-next=import-error
from asyncio import run
from dohome import discover_lights

async def main():
    """Discovers lights and prints information"""
    descriptions = await discover_lights("192.168.31.255")
    for descr in descriptions:
        print(f"IP: {descr['sta_ip']}")
        print(f"SID: {descr['sid']}")
        print(f"Chip: {descr['chip']}\n")

if __name__ == '__main__':
    run(main())
