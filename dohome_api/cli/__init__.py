"""DoHome CLI entrypoint"""
import logging
from arrrgs import arg, command, global_args, run

from dohome_api.discovery import discover_devices

from .light import turn_on, turn_off, color, white
from .describe import describe

global_args(
    arg('--hosts', '-d',
        default="all", help="Device hosts separated by comma. Default: all"),
    arg("--timeout", "-t",
        type=float, default=0.3, help="Discovery timeout in seconds"),
    arg("--debug", "-D",
        action="store_true", help="Enable debug logging")
)

@command()
async def discover():
    """Manifest creation"""
    devices = await discover_devices()
    if not devices:
        print("No devices found")
        return
    print(f"Found {len(devices)} devices")
    for device in devices:
        print(f"{device['ip']} {device['type'].name} {device['sid']}")

def _prepare(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    return args, None


def start():
    """Application entrypoint"""
    run(prepare=_prepare)
