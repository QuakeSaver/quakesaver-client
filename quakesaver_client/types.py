"""Module containing enums for various purposes."""

from enum import IntFlag


class PermissionLevel(IntFlag):
    """An enum to reflect the possible access level."""

    NONE = 0
    READ = 1
    EDIT = 2
    READ_EDIT = 3
    OWN = 4
    READ_OWN = 5
    EDIT_OWN = 6
    ALL = 7
