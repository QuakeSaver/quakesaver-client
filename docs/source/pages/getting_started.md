# Getting Started

## Setting up the client

`EMAIL` and `PASSWORD` correspond to the credentials you use to log in at [https://network.quakesaver.net](https://network.quakesaver.net).

```python
from quakesaver_client import QSClient

EMAIL = "user@yourorganisation.net"
PASSWORD = "!verstrongpassword1"

client = QSClient(email=EMAIL, password=PASSWORD)
```

## Full example script

Authenticate against the quakesaver server and download raw, as well as processed data.

Please note, that for security reasons each login session is only valid for 15 minutes. Thus, the client is not designed for long-term connections but for repeated queries.

```python
"""Example script for quakesaver_client usage."""

import sys
from datetime import datetime, timedelta
from pprint import pp

import obspy
from obspy import Stream

from quakesaver_client import QSClient
from quakesaver_client.models.measurement import MeasurementQuery

EMAIL = "user@yourorganisation.net"
PASSWORD = "!verstrongpassword1"
DATA_PATH = "./data"

client = QSClient(email=EMAIL, password=PASSWORD)

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

# Queries such as waveforms, station metadata and measurements (data products calculated on the sensor)
# require that you select a time window. We use that last 5 hours of data
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=5)

# Query RMS Amplitudes. In this case we calculate a rolling `mean` over 10 minutes time windows.
# Other `aggregators` are:
#  * None (default)
#  * max
#  * min
query = MeasurementQuery(
    start_time=start_time,
    end_time=end_time,
    measurement="rms_amplitude",
    field="rms_amplitude",
    interval=timedelta(minutes=10),
    aggregator="mean",
)
result = sensor.get_measurement(query)
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

# Download raw full waveforms from the sensor. Note that you can only query what is in the sensor's
# ringbuffer (usually the last ~ 48 hours). 
file_path = sensor.get_waveform_data(
    starttime=start_time, endtime=end_time, location_to_store=DATA_PATH
)

# Read the file into obspy for further processing...
stream: Stream = obspy.read(file_path)
for trace in stream.traces:
    print(trace.stats)
```
