"""FDSNWS client."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from io import BufferedWriter
from typing import Literal, Optional

import requests
from pydantic import BaseModel, Field, PositiveFloat, constr

from quakesaver_client.errors import NoDataError

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
    file: BufferedWriter,
) -> None:
    """Request FDSN waveform data of the sensor and stores in as a miniseed file."""
    logging.debug("requesting waveform data for sensor %s.", uri)
    response = requests.get(
        url=f"{uri}/fdsnws/dataselect/1/query",
        params=params.json(),
    )

    response.raise_for_status()
    if response.status_code in NoData.__args__:
        raise NoDataError(response.text)

    file.write(response.content)
