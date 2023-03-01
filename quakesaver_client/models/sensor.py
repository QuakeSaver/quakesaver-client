"""Module containing the sensor model."""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import requests
from pydantic import BaseModel, Extra, ValidationError

from quakesaver_client.errors import CorruptedDataError
from quakesaver_client.models.measurement import MeasurementQuery, MeasurementResult
from quakesaver_client.models.permission import Permission
from quakesaver_client.models.warnings import SensorWarnings
from quakesaver_client.types import StationDetailLevel
from quakesaver_client.util import handle_response


class Sensor(BaseModel):
    """A base schema for other schemas to derive from."""

    _headers: dict
    _api_base_url: str
    _fdsn_base_url: str

    uid: str
    software_version: str
    hardware_revision: str
    first_seen: datetime
    last_updated: datetime
    permission: Permission
    warnings: SensorWarnings
    max_data_product_count: int

    def __init__(self, api_base_url: str, fdsn_base_url: str, headers: dict, **data):
        """Create an instance of the class."""
        super().__init__(**data)
        self._headers = headers
        self._api_base_url = api_base_url
        self._fdsn_base_url = fdsn_base_url

    def get_data_product(self):
        """Request data products of the sensor."""
        pass

    def get_measurement(self, query: MeasurementQuery) -> MeasurementResult:
        """Request measurements of the sensor."""
        logging.debug("QSClient requesting measurement for sensor %s.", self.uid)
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

    def get_waveform_data(
        self,
        starttime: datetime,
        endtime: datetime,
        location_to_store: Path = None,
    ) -> Path | None:
        """Request FDSN waveform dat of the sensor."""
        logging.debug("QSClient requesting waveform data for sensor %s.", self.uid)

        if not location_to_store:
            location_to_store = Path(".")

        params = {"starttime": starttime, "endtime": endtime, "sensor_uids": self.uid}
        response = requests.get(
            url=f"{self._fdsn_base_url}/dataselect/1/queryauth_jwt_by_id",
            headers=self._headers,
            params=params,
        )

        if response.status_code != 200:
            raise CorruptedDataError(response.text)

        filename = response.headers["Content-Disposition"].split("=")[1]
        storage_path = location_to_store / filename
        with open(storage_path, "wb") as file:
            file.write(response.content)
        return storage_path

    def get_stationxml(
        self,
        starttime: datetime,
        endtime: datetime,
        minlatitude: float = -90,
        maxlatitude: float = 90,
        minlongitude: float = -180,
        maxlongitude: float = 180,
        level: StationDetailLevel = "station",
        location_to_store: Path = None,
    ) -> Path:
        """Request FDSN StationXML metadata of the sensor."""
        logging.debug("QSClient requesting stationxml for sensor %s.", self.uid)

        if not location_to_store:
            location_to_store = Path(".")

        params = {
            "starttime": starttime,
            "endtime": endtime,
            "sensor_uids": self.uid,
            "minlatitude": minlatitude,
            "maxlatitude": maxlatitude,
            "minlongitude": minlongitude,
            "maxlongitude": maxlongitude,
            "level": level,
        }
        response = requests.get(
            url=f"{self._fdsn_base_url}/station/1/queryauth_jwt_by_id",
            headers=self._headers,
            params=params,
        )

        if response.status_code != 200:
            raise CorruptedDataError(response.text)

        filename = response.headers["Content-Disposition"].split("=")[1]
        storage_path = location_to_store / filename
        with open(storage_path, "wb") as file:
            file.write(response.content)
        return storage_path

    class Config:  # noqa
        """Configuration subclass for pydantics BaseModel."""

        extra = Extra.allow
        underscore_attrs_are_private = True
