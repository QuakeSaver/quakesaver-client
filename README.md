# QuakeSaver Client

[![PyPI](https://img.shields.io/pypi/v/quakesaver-client)](https://pypi.org/project/quakesaver-client)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/quakesaver-client)
[![Test](https://github.com/QuakeSaver/quakesaver-client/actions/workflows/test.yml/badge.svg)](https://github.com/QuakeSaver/quakesaver-client/actions/workflows/test.yml)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

This is the client for the [QuakeSaver](https://quakesaver.net/) Sensor services.

You can find the documentation [here](https://quakesaver.github.io/quakesaver-client/).

## Getting Started

### Setting up the client

`EMAIL` and `PASSWORD` correspond to the credentials you use to log in at [https://network.quakesaver.net](https://network.quakesaver.net).

```python
from quakesaver_client import QSCloudClient

EMAIL = "user@yourorganisation.net"
PASSWORD = "!verstrongpassword1"

client = QSCloudClient(email=EMAIL, password=PASSWORD)
```

### Example to stream from the cloud

Authenticate against the quakesaver server and download raw, as well as processed data.

Please note, that for security reasons each login session is only valid for 15 minutes. Thus, the client is not designed for long-term connections but for repeated queries.

```python
"""Example script for quakesaver_client usage."""

import sys
from datetime import datetime, timedelta
from pprint import pp

import obspy
from obspy import Stream

from quakesaver_client import QSCloudClient
from quakesaver_client.models.data_product_query import DataProductQuery
from quakesaver_client.models.measurement import MeasurementQuery

EMAIL = "user@yourorganisation.net"
PASSWORD = "!verstrongpassword1"
DATA_PATH = "./data"

client = QSCloudClient(email=EMAIL, password=PASSWORD)

# Get a list of all available sensor IDs:
sensor_ids = client.get_sensor_ids()
pp(sensor_ids)

if len(sensor_ids) == 0:
    print("No sensors available")
    sys.exit()

# For demonstration, we use the first sensor in the list
sensor_uid_to_get = sensor_ids[0]

# Get the sensor from the client
sensor = client.get_sensor(sensor_uid_to_get)
pp(sensor.dict())

# Queries such as waveforms, station metadata and measurements (data products calculated
# on the sensor)
# require that you select a time window. We use that last 5 hours of data
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=5)

# Query various Measurements. In this case we calculate a rolling `mean` over 10 minutes
# time windows.
# Other `aggregators` are:
#  * None (default)
#  * max
#  * min
query = MeasurementQuery(
    start_time=start_time,
    end_time=end_time,
    interval=timedelta(minutes=10),
    aggregator="mean",
)
result = sensor.get_jma_intensity(query)
print(result)
result = sensor.get_peak_ground_acceleration(query)
print(result)
result = sensor.get_spectral_intensity(query)
print(result)
result = sensor.get_rms_offset(query)
print(result)

# Query various Data Products. You can only get 100 results at once, which is why there
# are limit and skip values. You can get data products from a specific time frame, by
# specifying start and end times.
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=5)
query = DataProductQuery(
    start_time=start_time,
    end_time=end_time,
    limit=100,
    skip=0,
)
result = sensor.get_event_records(query)
print(result)
result = sensor.get_hv_spectra(query)
print(result)
result = sensor.get_noise_autocorrelations(query)
print(result)

# Download station meta data as StationXML and store them in a local directory.
file_path = sensor.get_stationxml(
    starttime=start_time,
    endtime=end_time,
    level="response",
    location_to_store=DATA_PATH,
)
with open(file_path, "r") as file:
    print(file.read())

# Download raw full waveforms from the sensor. Note that you can only query what is in
# the sensor's ringbuffer (usually the last ~ 48 hours).
file_path = sensor.get_waveform_data(
    start_time=start_time, end_time=end_time, location_to_store=DATA_PATH
)

# Read the file into obspy for further processing...
stream: Stream = obspy.read(file_path)
for trace in stream.traces:
    print(trace.stats)
```

## `QSLocalClient` Examples

Interact with sensors on your local network using the `QSLocalClient`.

### Streaming Data

```python
import asyncio
from quakesaver_client import QSLocalClient


async def run():
    client = QSLocalClient()

    sensor = client.get_sensor("qssensor.local")
    stream = sensor.get_waveform_stream()
    async for chunk in stream.start():
        print(chunk)


asyncio.run(run())
```

### Downloading Data

Download the latest 10 minutes from a local sensor and write that into a file:

```python
import datetime
from quakesaver_client import QSLocalClient

client = QSLocalClient()
sensor = client.get_sensor("qssensor.local")

tmax = datetime.datetime.utcnow()
tmin = tmax - datetime.timedelta(minutes=10)
file_path = sensor.get_waveform_data(tmin, tmax)
print(file_path)
```
