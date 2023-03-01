"""Module containing authentication _token."""

from pydantic import BaseModel


class Token(BaseModel):
    """A class representing information about _token."""

    access_token: str
    token_type: str
