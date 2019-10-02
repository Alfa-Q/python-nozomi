"""Helper functions for creating paths and input normalization.

Primarily used by the nozomi API functions for generating the appropriate paths to files, and
ensuring that queries are made in a particular format used by the website.

If this package grows more complex, the functionality can be divided in a more manner. Due to
the simplicity of the current API, there isn't really a point right now.

TODO: Use logging and add logging support.

"""

import re
import urllib
import logging

from nozomi.exceptions import InvalidTagFormat


_LOGGER = logging.getLogger(__name__)


def sanitize_tag(tag: str) -> str:
    """Remove and replace any invalid characters in the tag.

    Args:
        tag: The search tag.

    Raises:
        InvalidTagFormat: If the tag is an empty string or begins with an invalid character.

    Returns:
        A tag in a valid format.

    """
    sanitized_tag = tag.lower().strip()
    sanitized_tag = re.sub('[/#%]', '', sanitized_tag)
    if not sanitized_tag:
        raise InvalidTagFormat(f"The tag '{tag}' is invalid. Cannot be empty after sanitization.")
    if sanitized_tag[0] == '-':
        raise InvalidTagFormat(f"The tag '{tag}' is invalid. Cannot begin with character '-'")
    return sanitized_tag


def create_tag_filepath(sanitized_tag: str) -> str:
    """Build the path to a .nozomi file for a particular tag.

    Every search tag/term has an associated .nozomi file stored in the database. Each file contains
    references to data that is related to the tag. This function builds the path to that file.

    Args:
        sanitized_tag: The sanitized search tag.

    Returns:
        The URL of the search tag's associated .nozomi file.

    """
    encoded_tag = urllib.parse.quote(sanitized_tag, safe='()')
    return f"https://j.nozomi.la/nozomi/{encoded_tag}.nozomi"
