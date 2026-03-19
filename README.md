# DoHome API

[![PyPI version](https://badge.fury.io/py/dohome-api.svg)](https://pypi.org/project/dohome-api/)
[![Quality assurance](https://github.com/mishamyrt/dohome_api/actions/workflows/qa.yaml/badge.svg?branch=main)](https://github.com/mishamyrt/dohome_api/actions/workflows/qa.yaml)

Async Python library for controlling smart LED bulbs and strips that use the DoIt protocol ([DoHome](https://apps.apple.com/app/dohome/id1374240531) app). Communicates with devices over the local network via TCP/UDP — no cloud required.

## Features

- Device discovery via UDP broadcast
- RGB color and white temperature control
- Brightness adjustment
- Built-in light effects (gradients, strobes, jumps)
- Device info, state reading, and power management
- Wi-Fi credential provisioning

## Installation

```
pip install dohome-api
```

Requires Python 3.12+.

## Quick Start

```python
import asyncio
from dohome.api import APIClient, discover
from dohome.transport import TCPStream, UDPBroadcast

async def main():
    # Discover devices on the local network
    broadcast = UDPBroadcast()
    devices = await discover(broadcast)
    broadcast.close()

    if not devices:
        print("No devices found")
        return

    # Connect to the first device
    client = APIClient(TCPStream(devices[0]["sta_ip"]))

    await client.set_power(True)
    await client.set_color((255, 0, 0), 128)  # Red at 50% brightness
    await asyncio.sleep(2)
    await client.set_power(False)

asyncio.run(main())
```

More examples (device info, Wi-Fi setup, state inspection) are available in the [`examples/`](./examples/) directory.

## Provisioning

You can use this library to perform the initial device setup without using the DoHome app.

To do this:

1. Clone this repository
2. Install dependencies with `make configure` command
3. Set the `DOHOME_SSID` and `DOHOME_PASSWORD` environment variables
4. Connect to the light bulb's access point
5. Run `uv run examples/configure.py`

## API Reference

### Discovery

| Function | Description |
|---|---|
| `discover(transport)` | Finds all DoIt devices on the local network |

### `APIClient`

| Method | Description |
|---|---|
| `set_power(is_on)` | Turn the device on or off |
| `set_color(rgb, brightness)` | Set RGB color with brightness (0–255) |
| `set_white(kelvin, brightness)` | Set white temperature (3000–6400 K) with brightness |
| `set_effect(effect)` | Activate a built-in light effect |
| `get_state()` | Read current light state |
| `get_device_info()` | Read device hardware info |
| `get_datetime()` / `set_datetime(dt)` | Read or set the device clock |
| `set_wifi_credentials(ssid, password)` | Provision Wi-Fi credentials |
| `reboot()` | Reboot the device |

## License

[MIT](./LICENSE) © Mikhael Khrustik
