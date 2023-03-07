"""This module provides schemas to query Data Products."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, root_validator
from pydantic.main import ModelMetaclass

from quakesaver_client.models.data_products import (
    EventRecord,
    HVSpectra,
    NoiseAutocorrelation,
)


class DataProductQuery(BaseModel):
    """A schema for querying data products."""

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    skip: conint(ge=0) = 0
    limit: conint(ge=1, le=100) = 100

    @root_validator(pre=True)
    def validate_interval_aggregator(cls: ModelMetaclass, values: dict) -> dict:
        """Assure start time is before end time."""
        if (
            "start_time" in values
            and values["start_time"] is not None
            and "end_time" in values
            and values["end_time"] is not None
        ):
            if values["start_time"] > values["end_time"]:
                raise ValueError("End time must be after start time.")
        return values


class DataProductQueryResult(BaseModel):
    """A return schema for the data products endpoint including data and metadata."""

    count: int
    ttl_seconds: int
    limit: int
    skip: int
    query_time_seconds: float


class NoiseAutocorrelationQueryResult(DataProductQueryResult):
    """A return schema for the Noise Autocorrelation results."""

    data_products: list[NoiseAutocorrelation]


class EventRecordQueryResult(DataProductQueryResult):
    """A return schema for the Event Record results."""

    data_products: list[EventRecord]


class HVSpectraQueryResult(DataProductQueryResult):
    """A return schema for the HV Spectra results."""

    data_products: list[HVSpectra]
