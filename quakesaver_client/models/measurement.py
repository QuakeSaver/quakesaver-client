"""This module provides schemas to interact with the InfluxDB."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal, Optional

from pydantic import BaseModel, constr, root_validator
from pydantic.main import ModelMetaclass

InfluxAggregator = Literal[
    "median",
    "mean",
    "first",
    "last",
    "min",
    "max",
    "count",
    "unique",
]


class MeasurementQuery(BaseModel):
    """A schema for querying measurements."""

    start_time: datetime
    end_time: datetime
    interval: Optional[timedelta] = None
    aggregator: Optional[InfluxAggregator] = None

    @root_validator(pre=True)
    def validate_interval_aggregator(cls: ModelMetaclass, values: dict) -> dict:
        """Assure that aggregators and intervals are only used together."""
        if "aggregator" in values and "interval" not in values:
            raise ValueError("aggregators need an interval")
        if "interval" in values and "aggregator" not in values:
            raise ValueError("intervals only work with aggregators")
        return values


class MeasurementQueryFull(BaseModel):
    """A schema for querying measurements."""

    start_time: datetime
    end_time: datetime
    measurement: constr(regex="^[a-zA-Z_-]*$")  # noqa: F722
    field: constr(regex="^[a-zA-Z_-]*$")  # noqa: F722
    interval: Optional[timedelta] = None
    aggregator: Optional[InfluxAggregator] = None

    @root_validator(pre=True)
    def validate_interval_aggregator(cls: ModelMetaclass, values: dict) -> dict:
        """Assure that aggregators and intervals are only used together."""
        if "aggregator" in values and "interval" not in values:
            raise ValueError("aggregators need an interval")
        if "interval" in values and "aggregator" not in values:
            raise ValueError("intervals only work with aggregators")
        return values


class InfluxData(BaseModel):
    """A schema to describe influx data points.

    The attribute naming is chosen for compatibility reasons with the frontend lib
    (ApexCharts).
    """

    times: list[datetime]
    values: list[float]


class MeasurementResult(BaseModel):
    """A return schema for the measurements endpoint including data and metadata."""

    sensor_uid: str
    query_time_seconds: float
    query: MeasurementQueryFull
    data: InfluxData
