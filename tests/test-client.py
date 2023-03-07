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
        base_domain=os.environ.get("TEST_CLIENT_DOMAIN"),
    )
    yield client


@pytest.fixture
def sensor(client):
    sensor_uids = client.get_sensor_ids()

    if len(sensor_uids) == 0:
        raise Exception("No sensors associated with this user account!")

    logging.info(f"Test sensor: {sensor_uids[0]}")
    yield client.get_sensor(sensor_uids[0])


def test_sensor_first_seen(sensor):
    assert isinstance(sensor.first_seen, datetime.datetime)
