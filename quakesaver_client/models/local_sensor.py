"""Sensor on the local network."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import requests
from obspy import Stream, read
from pydantic import Extra

from quakesaver_client.client_websocket import WebsocketHandler
from quakesaver_client.fdsnws import FDSNWSDataselectQuery
from quakesaver_client.fdsnws import dataselect as fdsnws_dataselect
from quakesaver_client.models.data_product_query import (
    DataProductQuery,
    EventRecordQueryResult,
    HVSpectraQueryResult,
    NoiseAutocorrelationQueryResult,
)
from quakesaver_client.models.measurement import (
    MeasurementQuery,
    MeasurementQueryFull,
    MeasurementResult,
)
from quakesaver_client.models.sensor_state import SensorState
from quakesaver_client.types import StationDetailLevel


class LocalSensor(SensorState):
    """A base schema for other schemas to derive from."""

    def __init__(self: LocalSensor, **data: dict) -> None:
        """Create an instance of the class."""
        super().__init__(**data)
        self._url = None

    @classmethod
    def get_sensor(cls: LocalSensor, sensor_url: str) -> LocalSensor:
        """Get a sensor which is available at `sensor_url`."""
        url = f"http://{sensor_url}/state"
        response = requests.get(url)
        sensor = LocalSensor.parse_raw(response.text)
        sensor._url = sensor_url
        return sensor

    def _get_data_product(
        self: LocalSensor,
        data_product_name: str,
        query: DataProductQuery,
    ) -> dict:
        """Request data products of the sensor."""
        ...

    def get_event_records(
        self: LocalSensor, query: DataProductQuery
    ) -> EventRecordQueryResult:
        """Get Event Records of the sensor.

        Args:
            query: The query parameters like time limit and time frame.

        Returns:
            EventRecordQueryResult: The queried data products.
        """
        ...

    def get_hv_spectra(
        self: LocalSensor, query: DataProductQuery
    ) -> HVSpectraQueryResult:
        """Get HV Spectres of the sensor.

        Args:
            query: The query parameters like time limit and time frame.

        Returns:
            HVSpectraQueryResult: The queried data products.
        """
        ...

    def get_noise_autocorrelations(
        self: LocalSensor, query: DataProductQuery
    ) -> NoiseAutocorrelationQueryResult:
        """Get the Event Records of the sensor.

        Args:
            query: The query parameters like time limit and time frame.

        Returns:
            NoiseAutocorrelationQueryResult: The queried data products.
        """
        ...

    def _get_measurement(
        self: LocalSensor, query: MeasurementQueryFull
    ) -> MeasurementResult:
        """Request measurements of the sensor."""
        ...

    def get_peak_horizontal_acceleration(
        self: LocalSensor, query: MeasurementQuery
    ) -> MeasurementResult:
        """Get the PGA measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_jma_intensity(
        self: LocalSensor, query: MeasurementQuery
    ) -> MeasurementResult:
        """Get the JMA Intensity measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_rms_amplitude(
        self: LocalSensor, query: MeasurementQuery
    ) -> MeasurementResult:
        """Get the RMS Amplitude measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_spectral_intensity(
        self: LocalSensor, query: MeasurementQuery
    ) -> MeasurementResult:
        """Get the Spectral Intensity measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_rms_offset(self: LocalSensor, query: MeasurementQuery) -> MeasurementResult:
        """Get the RMS Offset measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_waveform_stream(self: LocalSensor) -> WebsocketHandler:
        """Get a `WebsocketHandler` to serve waveform data."""
        return WebsocketHandler(self._url)

    def get_waveform_data(
        self: LocalSensor,
        file: Path,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> Path:
        """Request FDSN waveform dat of the sensor."""
        logging.debug("QSLocalClient requesting waveform data for sensor %s.", self.uid)

        end_time = end_time or datetime.now(tz=timezone.utc)
        params = FDSNWSDataselectQuery(starttime=start_time, endtime=end_time)

        if file.is_dir():
            filename = file / f"mseed-tmp-{uuid4()}"
        else:
            filename = file

        with filename.open("rb") as buffer:
            out_name = fdsnws_dataselect(
                uri=f"http://{self._url}",
                params=params,
                buffer=buffer,
            )

        if file.is_dir():
            filename.rename(out_name)
        return file

    def get_waveforms_obspy(
        self: LocalSensor,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> Stream:
        logging.debug("QSLocalClient requesting waveform data for sensor %s.", self.uid)

        end_time = end_time or datetime.now(tz=timezone.utc)
        params = FDSNWSDataselectQuery(starttime=start_time, endtime=end_time)

        buffer = BytesIO()
        fdsnws_dataselect(
            uri=f"http://{self._url}",
            params=params,
            buffer=buffer,
        )
        buffer.flush()
        buffer.seek(0)

        return read(buffer)

    def get_stationxml(
        self: LocalSensor,
        start_time: datetime,
        end_time: datetime,
        minlatitude: float = -90,
        maxlatitude: float = 90,
        minlongitude: float = -180,
        maxlongitude: float = 180,
        level: StationDetailLevel = "station",
        location_to_store: Path | str = None,
    ) -> Path:
        """Request FDSN StationXML metadata of the sensor."""
        ...

    class Config:  # noqa
        """Configuration subclass for pydantics BaseModel."""

        extra = Extra.allow
        underscore_attrs_are_private = True
