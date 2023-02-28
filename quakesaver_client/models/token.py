"""Module containing authentication token."""

from pydantic import BaseModel


class Token(BaseModel):
    """A class representing information about token."""

    access_token: str
    token_type: str
