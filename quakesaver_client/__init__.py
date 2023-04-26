"""Package containing a client for the QuakeSaver application."""
from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable, TypeVar

import requests
from pydantic import ValidationError

from quakesaver_client.errors import (
    CorruptedDataError,
)
from quakesaver_client.models.cloud_sensor import CloudSensor
from quakesaver_client.models.local_sensor import LocalSensor
from quakesaver_client.models.token import Token
from quakesaver_client.util import handle_response

DecoratedFunction = TypeVar("DecoratedFunction", bound=Callable[..., Any])


def _needs_token(function: DecoratedFunction) -> DecoratedFunction:
    @wraps(function)
    def request_token_if_needed(
        self: QSCloud, *args: list, **kwargs: dict
    ) -> DecoratedFunction:
        if not self._token:
            logging.debug("QSCloud requesting user _token.")
            response = requests.post(
                url=f"{self._api_base_url}/user/get_token",
                data=f"username={self._email}&password={self._password}",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response_data = handle_response(response)
            try:
                token = Token(**response_data)
            except ValidationError as e:
                raise CorruptedDataError() from e
            self._token = token

        return function(self, *args, **kwargs)

    return request_token_if_needed


class QSCloud:
    """A class representing a client to the backend."""

    _base_domain: str

    _email: str
    _password: str
    _token: Token | None

    _api_base_url: str
    _fdsn_base_url: str

    def __init__(
        self: QSCloud,
        email: str,
        password: str,
        base_domain: str | None = "network.quakesaver.net",
    ) -> None:
        """Create an instance of the class.

        Args:
            email: The _email address used to authenticate at the backend.
            password: The _password used to authenticate at the backend.
            base_domain: The base domain for the remote connection.
        """
        self._email = email
        self._password = password
        self._token = None

        self._base_domain = base_domain

        self._api_base_url = f"https://api.{base_domain}/api/v1"
        self._fdsn_base_url = f"https://fdsnws.{base_domain}/fdsnws"

    @_needs_token
    def _get_authorization_headers(self: QSCloud) -> dict:
        return {"Authorization": f"{self._token.token_type} {self._token.access_token}"}

    def get_sensor_ids(self: QSCloud) -> list[str]:
        """Fetch all sensor UIDs the user has access to.

        Returns:
            list[str]: The list of sensor UIDs.
        """
        logging.debug("QSCloud requesting sensor ids.")
        response = requests.get(
            url=f"{self._api_base_url}/user/me/sensors",
            headers=self._get_authorization_headers(),
        )
        response_data = handle_response(response)
        return list(response_data.keys())

    def get_sensor(self: QSCloud, sensor_uid: str) -> CloudSensor:
        """Fetch sensor data.

        Args:
            sensor_uid: The UID to request data from.

        Returns:
            CloudSensor: A sensor model to work with.
        """
        logging.debug("QSCloud requesting sensor %s.", sensor_uid)
        response = requests.get(
            url=f"{self._api_base_url}/sensors/{sensor_uid}",
            headers=self._get_authorization_headers(),
        )
        response_data = handle_response(response)
        try:
            sensor = CloudSensor(
                api_base_url=self._api_base_url,
                fdsn_base_url=self._fdsn_base_url,
                headers=self._get_authorization_headers(),
                **response_data,
            )
        except ValidationError as e:
            raise CorruptedDataError from e
        return sensor


class QSLocal:
    """Client to interact with sensors on your local network."""

    def get_sensor(self: QSLocal, sensor_url: str) -> LocalSensor:
        """Get a `LocalSensor` from the url."""
        url = f"http://{sensor_url}/state"
        response = requests.get(url)
        sensor = LocalSensor.parse_raw(response.text)
        sensor.url = sensor_url
        return sensor
