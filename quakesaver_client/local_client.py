from __future__ import annotations
from datetime import datetime
from pathlib import Path

from pydantic import Extra

from quakesaver_client import Sensor
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
from quakesaver_client.models.sensor_state import SensorState
from quakesaver_client.types import StationDetailLevel


class LocalSensor(SensorState):
    """A base schema for other schemas to derive from."""

    def __init__(self: Sensor, **data: dict) -> None:
        """Create an instance of the class."""
        super().__init__(**data)

    def _get_data_product(
        self: Sensor,
        data_product_name: str,
        query: DataProductQuery,
    ) -> dict:
        """Request data products of the sensor."""
        ...

    def get_event_records(
        self: Sensor, query: DataProductQuery
    ) -> EventRecordQueryResult:
        """Get Event Records of the sensor.

        Args:
            query: The query parameters like time limit and time frame.

        Returns:
            EventRecordQueryResult: The queried data products.
        """
        ...

    def get_hv_spectra(self: Sensor, query: DataProductQuery) -> HVSpectraQueryResult:
        """Get HV Spectres of the sensor.

        Args:
            query: The query parameters like time limit and time frame.

        Returns:
            HVSpectraQueryResult: The queried data products.
        """
        ...

    def get_noise_autocorrelations(
        self: Sensor, query: DataProductQuery
    ) -> NoiseAutocorrelationQueryResult:
        """Get the Event Records of the sensor.

        Args:
            query: The query parameters like time limit and time frame.

        Returns:
            NoiseAutocorrelationQueryResult: The queried data products.
        """
        ...

    def _get_measurement(
        self: Sensor, query: MeasurementQueryFull
    ) -> MeasurementResult:
        """Request measurements of the sensor."""
        ...

    def get_peak_horizontal_acceleration(
        self: Sensor, query: MeasurementQuery
    ) -> MeasurementResult:
        """Get the PGA measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_jma_intensity(self: Sensor, query: MeasurementQuery) -> MeasurementResult:
        """Get the JMA Intensity measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_rms_amplitude(self: Sensor, query: MeasurementQuery) -> MeasurementResult:
        """Get the RMS Amplitude measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_spectral_intensity(
        self: Sensor, query: MeasurementQuery
    ) -> MeasurementResult:
        """Get the Spectral Intensity measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_rms_offset(self: Sensor, query: MeasurementQuery) -> MeasurementResult:
        """Get the RMS Offset measurement of the sensor.

        Args:
            query: The query parameters like time frame and aggregator.

        Returns:
            MeasurementQuery: The queried data (if exists) as time series.
        """
        ...

    def get_waveform_data(
        self: Sensor,
        start_time: datetime,
        end_time: datetime,
        location_to_store: Path | str = None,
    ) -> Path | None:
        """Request FDSN waveform dat of the sensor."""
        ...

    def get_stationxml(
        self: Sensor,
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
