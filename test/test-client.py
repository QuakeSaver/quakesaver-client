import datetime

import pytest
import os
from quakesaver_client import QSClient


@pytest.fixture
def client():
    client = QSClient(
        email=os.environ.get("TEST_CLIENT_EMAIL"),
        password=os.environ.get("TEST_CLIENT_PASSWORD"),
    )
    yield client


@pytest.fixture
def sensor(client):
    yield client.get_sensor(client.get_sensor_ids()[0])


def test_sensor_first_seen(sensor):
    assert isinstance(sensor.first_seen, datetime.datetime)
