"""Manage sensor websocket connections."""
from __future__ import annotations

import base64
import gzip
import logging
from typing import Any, Generator

import aiohttp
import numpy as np

from quakesaver_client.models.data_products import DataUnit

from .models.data_products import TraceModel
from .models.websocket import WebSocketPayload, WebSocketRequest

logger = logging.getLogger(__name__)


DTYPE_MAP: dict[DataUnit, Any] = {
    DataUnit.counts: np.int32,
    DataUnit.m_s: float,
    DataUnit.m_s2: float,
}


START_ACTION = WebSocketRequest(action="startWaveformStream")
STOP_ACTION = WebSocketRequest(action="stopWaveformStream")


def convert_waveform_data(trace: TraceModel) -> None:
    """Inplace convert received binary channel data to numpy nd-arrays."""
    for channel, data in trace.data.items():
        if not isinstance(data, bytes):
            continue
        data = base64.b64decode(data)
        if trace.compressed:
            data = gzip.decompress(data)
        trace.data[channel] = np.frombuffer(data, dtype=DTYPE_MAP[trace.data_unit])


class WebsocketHandler:
    """Manage a sensor websocket connection."""

    def __init__(self: WebsocketHandler, url: str) -> None:
        """Initialize `WebsocketHandler`.

        Args:
            url: hostname (without protocol and route).
        """
        self._session = None
        self.url = url

    async def create_websocket(self: WebsocketHandler, session):
        async with session.ws_connect(f"ws://{self.url}/ws") as ws:
            await ws.send_str(START_ACTION.json())

            async for msg in ws:
                data = WebSocketPayload.parse_raw(msg.data)

                if "data" not in data.payload:
                    continue

                trace = TraceModel(**data.payload)
                convert_waveform_data(trace)
                logger.debug(f"received data from uid: {trace.uid}")
                yield trace

    def get_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def start(self: WebsocketHandler) -> Generator[TraceModel]:
        """Start the websocket connection."""
        session = self.get_session()
        async with session:
            while True:
                try:
                    async for trace in self.create_websocket(session):
                        yield trace
                except Exception as e:
                    logger.warning(f"{e}")

    async def stop(self: WebsocketHandler) -> None:
        """Stop the websocket connection."""
        session = self.get_session()
        async with session:
            async with session.ws_connect(f"ws://{self.url}/ws") as ws:
                await ws.send_str(STOP_ACTION.json())
