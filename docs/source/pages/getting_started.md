# Getting Started

## Set up the client

```python
from quakesaver_client import QSClient

EMAIL = "user@yourorganisation.net"
PASSWORD = "!verstrongpassword1"

client = QSClient(email=EMAIL, password=PASSWORD)
```

## Full example script

```python
"""Example script for quakesaver_client usage."""

import sys
from datetime import datetime, timedelta, timezone
from pprint import pp

import obspy
from obspy import Stream

from quakesaver_client import QSClient
from quakesaver_client.models.measurement import MeasurementQuery

EMAIL = "user@yourorganisation.net"
PASSWORD = "!verstrongpassword1"
DATA_PATH = "./data"

client = QSClient(email=EMAIL, password=PASSWORD)

########################################################################################
#                         List all available sensors                                   #
########################################################################################
sensor_ids = client.get_sensor_ids()
pp(sensor_ids)

########################################################################################
#                          Get sensor to work with                                     #
########################################################################################
if len(sensor_ids) == 0:
    print("No sensors available")
    sys.exit()

sensor_uid_to_get = sensor_ids[0]

sensor = client.get_sensor(sensor_uid_to_get)
pp(sensor.dict())

########################################################################################
#                          Load sensor measurement                                     #
########################################################################################
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=5)
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

########################################################################################
#                         Load StationXML meta data                                    #
########################################################################################
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=5)
file_path = sensor.get_stationxml(
    starttime=start_time,
    endtime=end_time,
    level="response",
    location_to_store=DATA_PATH,
)
with open(file_path, "r") as file:
    print(file.read())

########################################################################################
#                          Load FDSN waveform data                                     #
########################################################################################
end_time = datetime.now(tz=timezone.utc)
start_time = end_time - timedelta(hours=5)
file_path = sensor.get_waveform_data(
    starttime=start_time, endtime=end_time, location_to_store=DATA_PATH
)
stream: Stream = obspy.read(file_path)
for trace in stream.traces:
    print(trace.stats)
```
