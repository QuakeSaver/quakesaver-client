from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class ZMQChannel(BaseModel):
    deltat: float
    sample_unit: str
    sample_range: int
    nsamples: int
    dtype: str
    data: bytes


class ZMQDevice(BaseModel):
    recorder: str
    sensor: str
    network: str
    station: str
    location: str
    comment: str
    additional: dict


class ZMQPayload(BaseModel):
    version: int
    packet_timestamp: datetime
    starttime: datetime
    endtime: datetime
    latency: float
    deltat: float
    device: ZMQDevice
    channel_data: Dict[int, ZMQChannel]
