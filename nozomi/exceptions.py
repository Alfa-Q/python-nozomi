"""Nozomi exceptions."""

class NozomiException(Exception):
    """Base Nozomi package exception."""

class InvalidTagFormat(Exception):
    """The tag is not in valid format (i.e. empty string)."""
