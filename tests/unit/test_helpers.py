"""Test the functionality of the conversion functions."""

import logging

import pytest

from nozomi.helpers import (
    sanitize_tag,
    create_tag_filepath
)
from nozomi.exceptions import InvalidTagFormat


logger = logging.getLogger(__name__)


@pytest.mark.unit
@pytest.mark.parametrize('tag, expected', [
    ('shuten_douji_(fate/grand_order)', 'shuten_douji_(fategrand_order)'),
    ('オリジナル', 'オリジナル')
])
def test_sanitize_valid_tag(tag: str, expected: str):
    assert sanitize_tag(tag).casefold() == expected.casefold()


@pytest.mark.unit
@pytest.mark.parametrize('tag', ['', '/', '#', '//', '-'])
def test_sanitize_invalid_tag(tag: str):
    with pytest.raises(InvalidTagFormat):
        tag = sanitize_tag(tag)


@pytest.mark.unit
@pytest.mark.parametrize('tag, expected', [
    ('shuten_douji_(fategrand_order)', 'https://j.nozomi.la/nozomi/shuten_douji_(fategrand_order).nozomi'),
    ('testing123~/@', 'https://j.nozomi.la/nozomi/testing123~%2F%40.nozomi'),
    ('オリジナル', 'https://j.nozomi.la/nozomi/オリジナル.nozomi')
])
def test_generates_valid_address(tag: str, expected: str):
    assert create_tag_filepath(tag).casefold() == expected.casefold()
