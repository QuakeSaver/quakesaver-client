"""Package containing a client for the QuakeSaver application."""
from __future__ import annotations

import logging
from functools import wraps
from typing import Callable

import requests
from pydantic import ValidationError

from quakesaver_client.errors import (
    CorruptedDataError,
)
from quakesaver_client.models.sensor import Sensor
from quakesaver_client.models.token import Token
from quakesaver_client.util import handle_response


class QSClient:
    """A class representing a client to the backend."""

    base_domain: str

    email: str
    password: str
    token: Token | None

    api_base_url: str
    fdsn_base_url: str

    def __init__(
        self,
        email: str,
        password: str,
        base_domain: str | None = "network.quakesaver.net",
    ):
        """Create an instance of the class.

        Args:
            email: The email address used to authenticate at the backend.
            password: The password used to authenticate at the backend.
            base_domain: The base domain for the remote connection.
        """
        self.email = email
        self.password = password
        self.token = None

        self.base_domain = base_domain

        self.api_base_url = f"https://api.{base_domain}/api/v1"
        self.fdsn_base_url = f"https://fdsnws.{base_domain}/fdsnws"

    @staticmethod
    def _needs_token(function: Callable):
        @wraps(function)
        def request_token_if_needed(self: QSClient, *args, **kwargs):
            if not self.token:
                logging.debug("QSClient requesting user token.")
                response = requests.post(
                    url=f"{self.api_base_url}/user/get_token",
                    data=f"username={self.email}&password={self.password}",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response_data = handle_response(response)
                try:
                    token = Token(**response_data)
                except ValidationError as e:
                    raise CorruptedDataError() from e
                self.token = token

            return function(self, *args, **kwargs)

        return request_token_if_needed

    @_needs_token
    def _get_authorization_headers(self) -> dict:
        return {"Authorization": f"{self.token.token_type} {self.token.access_token}"}

    def get_sensor_ids(self) -> list[str]:
        """Fetch all sensor UIDs the user has access to.

        Returns:
        -------
            list[str]: The list of sensor UIDs.
        """
        logging.debug("QSClient requesting sensor ids.")
        response = requests.get(
            url=f"{self.api_base_url}/user/me/sensors",
            headers=self._get_authorization_headers(),
        )
        response_data = handle_response(response)
        return list(response_data.keys())

    def get_sensor(self, sensor_uid) -> Sensor:
        """Fetch sensor data.

        Args:
            sensor_uid: The UID to request data from.

        Returns:
        -------
            Sensor: A sensor model to work with.
        """
        logging.debug("QSClient requesting sensor %s.", sensor_uid)
        response = requests.get(
            url=f"{self.api_base_url}/sensors/{sensor_uid}",
            headers=self._get_authorization_headers(),
        )
        response_data = handle_response(response)
        try:
            sensor = Sensor(
                api_base_url=self.api_base_url,
                headers=self._get_authorization_headers(),
                **response_data,
            )
        except ValidationError as e:
            raise CorruptedDataError from e
        return sensor
