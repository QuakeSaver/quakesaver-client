import asyncio
import logging
from typing import Any, Union

import aiohttp
from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class SensorActor:

    uid: Union[str, None]

    def __init__(self, ip_address: str, uid: Union[str, None] = None) -> None:
        """A SensorActor interfaces a sensor on the local network."""
        self.ip = ip_address
        self.uid = uid

        self._logger = logger.getChild(ip_address)

    async def ping(self) -> None:
        """Retrieve state from sensor's websocket."""
        async with ClientSession() as session:
            async with session.ws_connect(f"http://{self.ip}:5533/ws") as ws:
                await ws.ping()
                await ws.close()

    async def get_state(self) -> Any:
        """Retrieve state from sensor's websocket."""
        async with ClientSession() as session:
            response = await session.get(f"http://{self.ip}:5533/state")
            return await response.json()

    async def is_alive(self) -> bool:
        """Check if sensor is alive.

        Returns:
            bool: Alive state.
        """
        try:
            await asyncio.wait_for(self.ping(), timeout=1.0)
            return True
        except aiohttp.client_exceptions.ClientConnectorError as e:
            logger.debug(e)
        except TimeoutError as e:
            logger.info(e)
            return False
        except Exception as e:
            logger.debug(e)
            return False
