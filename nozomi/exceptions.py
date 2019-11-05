"""Nozomi exceptions."""

class NozomiException(Exception):
    """Base Nozomi package exception."""

class InvalidTagFormat(NozomiException):
    """The tag is not in valid format (i.e. empty string)."""

class InvalidArgument(NozomiException):
    """The argument provided is invalid."""
