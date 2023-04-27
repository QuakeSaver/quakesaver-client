"""local sensor tests."""
import pytest

from quakesaver_client import QSLocalClient


@pytest.mark.local
async def test_locally() -> None:
    """Connect to a sensor on the local network."""
    client = QSLocalClient()
    sensor = client.get_sensor("qssensor.local")
    stream = sensor.get_waveform_stream()

    async for trace_segment in stream.start():
        if trace_segment:
            await stream.stop()
            break
