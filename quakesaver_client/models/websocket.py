"""Websocket data types."""

from typing import Any, Literal

from pydantic import BaseModel


class WebSocketRequest(BaseModel):
    """Action to start and stop the websocket on the sensor end."""

    action: Literal["startWaveformStream", "stopWaveformStream"]


class WebSocketPayload(BaseModel):
    """Data sent via websocket from a sensor."""

    version: int = 1
    mutation: str
    class_name: str = "none"
    payload: Any
