from .models.websocket import *
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


START_ACTION = WebSocketRequest(action="startWaveformStream")
STOP_ACTION = WebSocketRequest(action="stopWaveformStream")


class WebsocketHandler:
    def __init__(self, url):
        self.session = None
        self.url = url

    async def start(self):
        self.session = aiohttp.ClientSession()
        async with self.session:
            async with self.session.ws_connect(f"ws://{self.url}/ws") as ws:
                try:
                    await ws.send_str(START_ACTION.json())

                    async for msg in ws:
                        data = WebSocketPayload.parse_raw(msg.data)

                        if "data" not in data.payload:
                            continue

                        waveforms = payload_to_waveforms(data)
                        logger.info(f"received {waveforms}")
                        yield waveforms
                except Exception as e:
                    await ws.send_str(STOP_ACTION.json())
                    raise e

    async def stop(self):
        if self.session is None:
            logger.info("no waveform stream session")

        async with self.session:
            async with self.session.ws_connect(f"ws://{self.url}/ws") as ws:
                await ws.send_str(STOP_ACTION.json())
