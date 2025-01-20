"""Light handlers for the DoHome CLI"""

from arrrgs import arg, command
from .batch import get_devices, parallel_run

def _hex_to_rgb(hex_color):
    """Converts hex color to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color")

    r, g, b = hex_color[:2], hex_color[2:4], hex_color[4:]
    return (
        int(r, 16),
        int(g, 16),
        int(b, 16)
    )

@command()
async def turn_off(args):
    """Turn off the device(s)"""
    devices = await get_devices(args)
    await parallel_run(lambda x: x.set_power(False), devices)

@command()
async def turn_on(args):
    """Turn off the device(s)"""
    devices = await get_devices(args)
    await parallel_run(lambda x: x.set_power(True), devices)

@command(
    arg("color", type=str, help="HEX color value"),
    arg("--brightness", "-b", type=int, default=255, help="0-255 brightness value"),
)
async def color(args):
    """Turn off the device(s)"""
    devices = await get_devices(args)
    try:
        rgb_color = _hex_to_rgb(args.color)
    except ValueError:
        print("Invalid hex color")
        return
    await parallel_run(
        lambda x: x.set_color(rgb_color, args.brightness), devices)

@command(
    arg("kelvin", type=int, help="Kelvin color temperature"),
    arg("--brightness", "-b", type=int, default=255, help="0-255 brightness value"),
)
async def white(args):
    """Turn off the device(s)"""
    devices = await get_devices(args)
    await parallel_run(
        lambda x: x.set_white_temperature(args.kelvin, args.brightness), devices)
