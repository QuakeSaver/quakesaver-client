from quakesaver_client import QSLocal


async def test_locally():
    client = QSLocal()
    sensor = client.get_sensor("qssensor.local")
    stream = sensor.get_waveform_stream()
    async for chunk in stream.start():
        if chunk:
            await stream.stop()
            break
