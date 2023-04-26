from models.websocket import *
import gzip

import aiohttp
import base64
import numpy as np
import logging

logger = logging.getLogger(__name__)


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
