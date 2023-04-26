from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path

import aiohttp
from pydantic import Extra

from quakesaver_client.client_websocket import WebsocketHandler
from quakesaver_client.models.data_product_query import (
    DataProductQuery,
    EventRecordQueryResult,
    HVSpectraQueryResult,
    NoiseAutocorrelationQueryResult,
)
from quakesaver_client.models.measurement import (
    MeasurementResult,
    MeasurementQueryFull,
    MeasurementQuery,
)
import requests
from quakesaver_client.models.sensor_state import SensorState
from quakesaver_client.types import StationDetailLevel


class LocalSensor(SensorState):
    """A base schema for other schemas to derive from."""

    def __init__(self: LocalSensor, **data: dict) -> None:
        """Create an instance of the class."""
        super().__init__(**data)
        self.url = None

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

    def get_waveform_stream(self):
        return WebsocketHandler(self.url)

    def get_waveform_data(
        self: LocalSensor,
        start_time: datetime,
        end_time: datetime,
        location_to_store: Path | str = None,
    ) -> Path | None:
        """Request FDSN waveform dat of the sensor."""
        ...

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


#
# async def main():
#     url = "qssensor.local"
#     sensor = await get_sensor(url)
#     async for chunk in sensor.stream_waveform_data():
#         print(chunk)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)
#     asyncio.run(main())
