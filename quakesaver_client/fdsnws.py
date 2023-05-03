"""FDSNWS client."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import BinaryIO, Literal, Optional, get_args

import requests
from pydantic import BaseModel, Field, PositiveFloat, constr

from quakesaver_client.errors import NoDataError

NoData = Literal[204, 404]  # HTTP Error codes
DataFormat = Literal["miniseed"]


class FDSNWSDataselectQuery(BaseModel):
    """Query for fdsn requests against QuakeSaver local and cloud endpoints."""

    starttime: Optional[datetime] = None
    endtime: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Add Set
    # Reference http://www.fdsn.org/pdf/SEEDManual_V2.4.pdf [p37]
    network: constr(max_length=2) = "*"
    station: constr(max_length=5) = "*"
    location: constr(max_length=2) = "*"
    channel: constr(max_length=3) = "*"

    longestonly: bool = True

    format: DataFormat = "miniseed"


def dataselect(
    uri: str,
    params: FDSNWSDataselectQuery,
    buffer: BinaryIO,
) -> str:
    """Request FDSN waveform data of the sensor and stores in as a MiniSEED file."""
    logging.debug("requesting waveform data for sensor %s.", uri)
    response = requests.get(
        url=f"{uri}/fdsnws/dataselect/1/query", params=params.dict()
    )

    if response.status_code in get_args(NoData):
        raise NoDataError(response.text)
    response.raise_for_status()

    try:
        filename = response.headers.get("Content-Disposition").split("=")[1].strip('"')
    except (KeyError, IndexError):
        filename = "qssensor-data.mseed"

    for content in response.iter_content(chunk_size=None):
        buffer.write(content)

    buffer.flush()
    return str(filename)
