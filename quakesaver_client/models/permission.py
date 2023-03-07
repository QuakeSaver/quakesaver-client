"""module containing permission models."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from quakesaver_client.types import PermissionLevel


class Permission(BaseModel):
    """A class to reflect permissions of a subject on an object."""

    groups: dict[str, PermissionLevel]
    primary_group: Optional[str]
