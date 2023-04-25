from pydantic import BaseModel
from typing import Literal, Any


class WebSocketRequest(BaseModel):
    action: Literal["startWaveformStream", "stopWaveformStream"]


class WebSocketPayload(BaseModel):
    version: int = 1
    mutation: str
    class_name: str = "none"
    payload: Any
