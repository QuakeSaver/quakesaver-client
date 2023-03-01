"""Shared utility functions."""
from requests import HTTPError, Response

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
    try:
        response.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            raise WrongAuthenticationError() from e
        if e.response.status_code == 422:
            raise CorruptedDataError() from e
        raise UnknownError() from e

    try:
        return response.json()
    except Exception as e:
        raise CorruptedDataError() from e
