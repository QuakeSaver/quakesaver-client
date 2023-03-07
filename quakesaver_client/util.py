"""Shared utility functions."""
from __future__ import annotations

from pathlib import Path

from requests import HTTPError, Response

from quakesaver_client.errors import (
    CorruptedDataError,
    InsufficientPermissionError,
    SessionExpiredError,
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
            reason = response.json()["detail"]
            if reason == "Insufficient permissions.":
                raise InsufficientPermissionError() from e
            if reason == "Session expired, please log in again.":
                raise SessionExpiredError() from e
            raise WrongAuthenticationError() from e
        if e.response.status_code == 422:
            raise CorruptedDataError() from e
        raise UnknownError() from e

    try:
        return response.json()
    except Exception as e:
        raise CorruptedDataError() from e


def assure_output_path(location_to_store: Path | str = None) -> Path:
    """Assure an output path is set and created.

    Args:
        location_to_store: The output path.

    Returns:
        Path: An existent path to store data.
    """
    if not location_to_store:
        location_to_store = Path(".")
    else:
        if isinstance(location_to_store, str):
            location_to_store = Path(location_to_store)
        location_to_store.mkdir(parents=True, exist_ok=True)
    return location_to_store
