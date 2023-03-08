"""Tests for the QuakeSaver client."""
import datetime
import logging
import os

import pytest

from quakesaver_client import QSClient, Sensor


@pytest.fixture
def client() -> QSClient:
    """Get a set-up client."""
    client = QSClient(
        email=os.environ.get("TEST_CLIENT_EMAIL"),
        password=os.environ.get("TEST_CLIENT_PASSWORD"),
        base_domain=os.environ.get("TEST_CLIENT_DOMAIN"),
    )
    yield client


@pytest.fixture
def sensor(client: QSClient) -> Sensor:
    """Get the first available sensor."""
    sensor_uids = client.get_sensor_ids()

    if len(sensor_uids) == 0:
        raise Exception("No sensors associated with this user account!")

    logging.info(f"Test sensor: {sensor_uids[0]}")
    yield client.get_sensor(sensor_uids[0])


def test_sensor_first_seen(sensor: Sensor) -> None:
    """Test that the sensors 'first_seen' attribute is set."""
    assert isinstance(sensor.first_seen, datetime.datetime)
