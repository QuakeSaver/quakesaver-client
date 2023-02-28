"""Shared utility functions."""
from requests import Response

from quakesaver_client.errors import (
    CorruptedDataError,
    UnknownError,
    WrongAuthenticationError,
)


def handle_response(response: Response) -> dict:
    """Parse check a response for encountered errors.

    Args:
        response: The response to check.

    Returns:
        dict: The loaded JSON response.
    """
    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            raise CorruptedDataError() from e
    if response.status_code == 401:
        raise WrongAuthenticationError()
    if response.status_code == 422:
        raise CorruptedDataError()
    raise UnknownError()
