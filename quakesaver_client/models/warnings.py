"""Module containing classes for handling sensor warnings.."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

WarningLevel = Literal["warning", "error", "critical"]


class SensorWarning(BaseModel):
    """A class representing a warning of the sensor."""

    created: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    message: str
    title: str
    level: WarningLevel = "warning"


class SensorWarnings(BaseModel):
    """A class representing warnings for the sensor."""

    data: dict[str, SensorWarning] = {}

    class Config:
        """Configuration subclass for pydantics BaseModel."""

        orm_mode = True
