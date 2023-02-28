"""Module containing common errors which occur during interaction with the system."""


class UnknownError(RuntimeError):
    """An error to raise if unknown problems occur."""


class WrongAuthenticationError(ValueError):
    """An error to raise if wrong authentication details where provided."""


class CorruptedDataError(ValueError):
    """An error to raise if data was incomplete or wrong."""
