"""FDSNWS client."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import IO, TYPE_CHECKING, BinaryIO, Literal, Optional

import requests
from pydantic import BaseModel, Field, PositiveFloat, constr

from quakesaver_client.errors import NoDataError

if TYPE_CHECKING:
    from io import BufferedWriter

NoData = Literal[204, 404]  # HTTP Error codes
DataFormat = Literal["miniseed"]
DataQuality = Literal["D", "R", "Q", "M", "B"]


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
    quality: DataQuality = "B"

    longestonly: bool = True
    minimumlength: PositiveFloat = 0.0

    format: DataFormat = "miniseed"
    nodata: NoData = 204


def dataselect(
    uri: str,
    params: FDSNWSDataselectQuery,
    buffer: BinaryIO,
) -> str:
    """Request FDSN waveform data of the sensor and stores in as a MiniSEED file."""
    logging.debug("requesting waveform data for sensor %s.", uri)
    response = requests.get(
        url=f"{uri}/fdsnws/dataselect/1/query",
        params=params.json(),
    )

    if response.status_code in get_args(NoData):
        raise NoDataError(response.text)
    response.raise_for_status()

    try:
        filename = response.headers.get("Content-Disposition").split("=")[1]
    except (KeyError, IndexError):
        filename = "qssensor-data.mseed"

    for content in response.iter_content(chunk_size=None):
        buffer.write(content)

    buffer.flush()
    return filename
