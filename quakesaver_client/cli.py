import asyncio
import logging
from functools import wraps
from typing import Optional

import click

from quakesaver_client.sensor_actor import SensorActor

logger = logging.getLogger("quakesaver_client")
logging.basicConfig(level=logging.DEBUG)


@click.option("--debug", is_flag=True, type=bool)
@click.group()
def cli(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def click_coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


async def probe_sensor(host):
    logger.debug(f"probing {host}")
    sensor = SensorActor(host)
    alive = await sensor.is_alive()
    if alive:
        state = await sensor.get_state()
        uid = state["uid"]
        version = state["software_version"]
        logger.info(f"Sensor {uid}@{host} (version {version}) is alive")
        return uid, host
    else:
        logger.debug("No running sensor software found on %s", host)


@cli.command()
@click.argument("hosts", default=None, required=False, type=str)
@click_coro
async def detect(hosts: Optional[str]) -> None:
    """Detect QuakeSaver sensors.

    Args:
        hosts (str): IP range to scan for sensors in CIDR notation.
        Defaults to local ip range.
    """
    logger.info(f"detecting hosts at {hosts}")
    if hosts is None:
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        hosts = local_ip + "/24"

    hosts_and_range = hosts.split("/")
    fn_alive_sensors = "sensors-alive.csv"

    host, ip_range = hosts_and_range
    host = host.split(".")[0:3]
    hosts = []
    for i in range(1, 256):
        hosts.append(f"{'.'.join(host)}.{i}")

    logger.info(f"scanning {len(hosts)} hosts")

    sensors = await asyncio.gather(*[probe_sensor(host) for host in hosts])
    sensors = [sensor for sensor in sensors if sensor]
    with open(fn_alive_sensors, "w") as f:
        f.write("uid,ip_address\n")
        for uid, ip_address in sensors:
            f.write(f"{uid},{ip_address}\n")

    logger.info(f"saved alive sensor list to {fn_alive_sensors}")
