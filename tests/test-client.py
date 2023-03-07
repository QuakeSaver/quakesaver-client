import datetime
import logging
import pytest
import os
from quakesaver_client import QSClient


@pytest.fixture
def client():
    client = QSClient(
        email=os.environ.get("TEST_CLIENT_EMAIL"),
        password=os.environ.get("TEST_CLIENT_PASSWORD"),
        base_domain=os.environ.get("TEST_CLIENT_DOMAIN")
    )
    yield client


@pytest.fixture
def sensor(client):
    sensor_uid = client.get_sensor_ids()[0]
    logging.info(f"Test sensor: {sensor_uid}")
    yield client.get_sensor(sensor_uid)


def test_sensor_first_seen(sensor):
    assert isinstance(sensor.first_seen, datetime.datetime)
