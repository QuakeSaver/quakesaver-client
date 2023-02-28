"""Module containing the sensor model."""
from datetime import datetime

import requests
from pydantic import BaseModel, Extra, ValidationError

from quakesaver_client.errors import CorruptedDataError
from quakesaver_client.models.measurement import MeasurementQuery, MeasurementResult
from quakesaver_client.models.permission import Permission
from quakesaver_client.models.warnings import SensorWarnings
from quakesaver_client.util import handle_response


class Sensor(BaseModel):
    """A base schema for other schemas to derive from."""

    _headers: dict
    _api_base_url: str

    uid: str
    software_version: str
    hardware_revision: str
    first_seen: datetime
    last_updated: datetime
    permission: Permission
    warnings: SensorWarnings
    max_data_product_count: int

    def __init__(self, api_base_url: str, headers: dict, **data):
        """Create an instance of the class."""
        super().__init__(**data)
        self._headers = headers
        self._api_base_url = api_base_url

    def get_data_product(self):
        """Request data products of the sensor."""
        pass

    def get_measurement(self, query: MeasurementQuery) -> MeasurementResult:
        """Request measurements of the sensor."""
        response = requests.post(
            url=f"{self._api_base_url}/sensors/{self.uid}/measurements",
            headers=self._headers,
            data=query.json(),
        )
        response_data = handle_response(response)
        try:
            result = MeasurementResult(**response_data)
        except ValidationError as e:
            raise CorruptedDataError() from e
        return result

    def get_waveform_data(self):
        """Request FDSN waveform dat of the sensor."""
        pass

    def get_stationxml(self):
        """Request FDSN StationXML metadata of the sensor."""
        pass

    class Config:  # noqa
        """Configuration subclass for pydantics BaseModel."""

        extra = Extra.allow
        underscore_attrs_are_private = True
