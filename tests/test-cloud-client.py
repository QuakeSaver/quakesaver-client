"""Tests for the QuakeSaver client."""
import logging
import os
from datetime import datetime, timedelta
from pathlib import PosixPath

import pytest

from quakesaver_client import CloudSensor, QSCloudClient
from quakesaver_client.models.measurement import (
    InfluxAggregator,
    MeasurementQuery,
    MeasurementResult,
)


@pytest.fixture
def client() -> QSCloudClient:
    """Get a set-up client."""
    client = QSCloudClient(
        email=os.environ.get("TEST_CLIENT_EMAIL"),
        password=os.environ.get("TEST_CLIENT_PASSWORD"),
        base_domain=os.environ.get("TEST_CLIENT_DOMAIN"),
    )
    yield client


@pytest.fixture
def sensor(client: QSCloudClient) -> CloudSensor:
    """Get the first available sensor."""
    sensor_uids = client.get_sensor_ids()

    if len(sensor_uids) == 0:
        raise Exception("No sensors associated with this user account!")

    logging.info(f"Test sensor: {sensor_uids[0]}")
    yield client.get_sensor(sensor_uids[0])


def test_sensor_first_seen(sensor: CloudSensor) -> None:
    """Test that the sensors 'first_seen' attribute is set."""
    assert isinstance(sensor.first_seen, datetime)


@pytest.mark.parametrize("aggregator", InfluxAggregator.__dict__["__args__"])
@pytest.mark.parametrize(
    "query_method",
    [
        "get_peak_horizontal_acceleration",
        "get_jma_intensity",
        "get_rms_amplitude",
        "get_spectral_intensity",
    ],
)
def test_data_products(sensor: CloudSensor, aggregator: str, query_method: str) -> None:
    """Test all dataproduct endpoints with all available aggregators."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    query = MeasurementQuery(
        start_time=start_time,
        end_time=end_time,
        interval=timedelta(minutes=5),
        aggregator=aggregator,
    )
    method = getattr(sensor, query_method)
    result = method(query)
    assert isinstance(result, MeasurementResult)


def test_waveforms(sensor: CloudSensor) -> None:
    """Test downloading raw waveforms."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    result = sensor.get_waveform_data(
        start_time=start_time,
        end_time=end_time,
    )
    assert isinstance(result, PosixPath)
