import asyncio
import base64

import zmq
import zmq.asyncio
import numpy as np
from models.zmq_payload import ZMQPayload
import logging

context = zmq.asyncio.Context()

logger = logging.getLogger(__name__)


async def listen_sensor(url="tcp://qssensor.local:5556"):
    subscriber = context.socket(zmq.SUB)

    subscriber.connect(url)
    subscriber.subscribe("")

    while True:
        message = await subscriber.recv_multipart()
        message = message[0]
        data = ZMQPayload.parse_raw(message.decode())

        channels = {}
        for channel, v in data.channel_data.items():
            waveform = base64.b64decode(v.data)
            waveform = np.frombuffer(waveform, dtype=np.dtype(v.dtype))
            channels[channel] = waveform
        logger.debug(f"received {channels}")

        yield channels


if __name__ == "__main__":

    async def run():
        async for _ in listen_sensor():
            ...

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(run())
