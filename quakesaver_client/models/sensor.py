"""Module containing the sensor model."""
from datetime import datetime

from pydantic import BaseModel, Extra

from quakesaver_client.models.permission import Permission
from quakesaver_client.models.warnings import SensorWarnings


class Sensor(BaseModel):
    """A base schema for other schemas to derive from."""

    _headers: str

    uid: str
    software_version: str
    hardware_revision: str
    first_seen: datetime
    last_updated: datetime
    permission: Permission
    warnings: SensorWarnings
    max_data_product_count: int

    def get_data_product(self):
        """Request data products of the sensor."""
        pass

    def get_measurement(self):
        """Request measurements of the sensor."""
        pass

    def get_waveform_data(self):
        """Request FDSN waveform dat of the sensor."""
        pass

    def get_stationxml(self):
        """Request FDSN StationXML metadata of the sensor."""
        pass

    class Config:  # noqa
        """Configuration subclass for pydantics BaseModel."""

        extra = Extra.allow
