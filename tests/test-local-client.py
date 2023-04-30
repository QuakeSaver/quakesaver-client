"""local sensor tests."""
import datetime

import pytest

from quakesaver_client import LocalSensor, QSLocalClient


@pytest.fixture()
def local_test_sensor() -> LocalSensor:
    client = QSLocalClient()
    sensor = client.get_sensor("localhost:5533")
    return sensor


@pytest.mark.skip
@pytest.mark.local
async def test_stream(local_test_sensor) -> None:
    """Connect to a sensor on the local network."""
    stream = local_test_sensor.get_waveform_stream()

    async for trace_segment in stream.start():
        assert not trace_segment.compressed
        print(trace_segment)
        # if trace_segment:
        #     await stream.stop()
        #     break


@pytest.mark.local
async def test_waveform_fetch(local_test_sensor) -> None:
    """Connect to a sensor on the local network."""
    tmax = datetime.datetime.utcnow()
    tmin = tmax - datetime.timedelta(hours=30)
    data = local_test_sensor.get_waveform_data(tmin, tmax)
    print(data)
