from models.websocket import *
import asyncio
import gzip

import aiohttp
import base64
import numpy as np
import logging

from quakesaver_client.local_client import LocalSensor
from quakesaver_client.models.sensor_state import SensorState

logger = logging.getLogger(__name__)


class DataHandler:
    def __init__(self, alert_callback):
        self.last = 0
        self.threshold = 10
        self.alert_callback = alert_callback

    async def data_callback(self, channels):
        x, y, z = channels["EN1"], channels["EN2"], channels["EN3"]
        x = x / x.mean()
        y = y / y.mean()
        z = z / z.mean()

        motion = np.sqrt(x**2 + y**2 + z**2)
        motion = motion.max()
        logger.debug(f"motion: {motion}")

        if self.last - motion > self.threshold:
            await self.alert_callback(motion)

        self.last = motion


def payload_to_waveforms(data):
    waveforms = data.payload["data"]
    compressed = bool(data.payload["compressed"])
    all_channels = {}
    for channel, v in waveforms.items():
        v = base64.b64decode(v)
        if compressed:
            v = gzip.decompress(v)

        data = np.frombuffer(v, dtype=np.int32)
        all_channels[channel] = data

    return all_channels


async def get_sensor(sensor_url):
    async with aiohttp.ClientSession() as client:
        async with client.get(f"http://{sensor_url}/state") as resp:
            state = await resp.text()
            return LocalSensor.parse_raw(state)


async def start_event_trigger_listener(sensor_url):
    start_action = WebSocketRequest(action="startWaveformStream")

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"ws://{sensor_url}/ws") as ws:
            await ws.send_str(start_action.json())

            async for msg in ws:
                data = WebSocketPayload.parse_raw(msg.data)

                if "data" not in data.payload:
                    continue

                waveforms = payload_to_waveforms(data)
                logger.info(f"received {waveforms}")
                yield waveforms


async def main():
    url = "qssensor.local"
    await get_sensor(url)
    async for _ in start_event_trigger_listener(url):
        ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
