"""DoHome batch operations"""
from typing import TypeVar, Iterable, Callable
import asyncio

from dohome_api.device import open_device, DoHomeDevice
from dohome_api.discovery import discover_devices



async def _open_devices(hosts: list[str]) -> list[DoHomeDevice]:
    """Connects to the DoHome devices"""
    return map(open_device, hosts)

async def _discover_ips(timeout: float):
    devices = await discover_devices(timeout=timeout)
    return map(lambda x: x["ip"], devices)

def _parse_hosts(hosts: str) -> list[str]:
    hosts = map(lambda x: x.strip(), hosts.split(","))
    hosts = filter(lambda x: x != "", hosts)
    return hosts

async def get_devices(args) -> list[DoHomeDevice]:
    """Opens DoHome devices from args"""
    if args.hosts == "all":
        hosts = await _discover_ips(args.timeout)
    else:
        hosts = _parse_hosts(args.hosts)
    return await _open_devices(hosts)

T = TypeVar('T')
R = TypeVar('R')

async def parallel_run(func: Callable[[T], R], args: Iterable[T]) -> Iterable[R]:
    """Runs multiple functions in parallel"""
    return await asyncio.gather(*map(func, args))
