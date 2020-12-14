"""Test the functionality of the conversion functions."""

import pytest

from nozomi.helpers import sanitize_tag, create_tag_filepath, create_post_filepath, parse_post_id
from nozomi.exceptions import InvalidTagFormat, InvalidUrlFormat


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
        sanitize_tag(tag)


@pytest.mark.unit
@pytest.mark.parametrize('url, expected', [
    ('https://nozomi.la/post/26945941.html#sakimichan', 26945941),
    ('https://nozomi.la/post/26945920.html#sakimichan', 26945920),
    ('https://nozomi.la/post/26905532.html#veigar', 26905532)
])
def test_parse_post_id_valid(url: str, expected: int):
    assert parse_post_id(url) == expected


@pytest.mark.unit
@pytest.mark.parametrize('url', [
    'https://i.nozomi.la/b/d0/fcedb19b290f62136c304480d1aa18ab98caee262b97a519ccf289fb0f56dd0b.jpg',
    'https://i.nozomi.la/a/5c/49c8946c0f173c536e3735555d8e451526d845ebe07e09773927009db38ae5ca.jpg'
])
def test_parse_post_id_invalid(url: str):
    with pytest.raises(InvalidUrlFormat):
        parse_post_id(url)


@pytest.mark.unit
@pytest.mark.parametrize('tag, expected', [
    ('shuten_douji_(fategrand_order)', 'https://j.nozomi.la/nozomi/shuten_douji_(fategrand_order).nozomi'),
    ('testing123~/@', 'https://j.nozomi.la/nozomi/testing123~%2F%40.nozomi'),
    ('オリジナル', 'https://j.nozomi.la/nozomi/オリジナル.nozomi')
])
def test_generates_valid_tag_address(tag: str, expected: str):
    assert create_tag_filepath(tag).casefold() == expected.casefold()


@pytest.mark.unit
@pytest.mark.parametrize('tag', [''])
def test_generates_invalid_tag_address(tag: str):
    with pytest.raises(InvalidTagFormat):
        create_tag_filepath(tag)


@pytest.mark.unit
@pytest.mark.parametrize('post_id, expected', [
    (5,         'https://j.nozomi.la/post/5.json'),
    (42,        'https://j.nozomi.la/post/42.json'),
    (100,       'https://j.nozomi.la/post/0/10/100.json'),
    (4269,      'https://j.nozomi.la/post/9/26/4269.json'),
    (9017646,   'https://j.nozomi.la/post/6/64/9017646.json'),
    (8419981,   'https://j.nozomi.la/post/1/98/8419981.json'),
    (8037229,   'https://j.nozomi.la/post/9/22/8037229.json'),
    (8012806,   'https://j.nozomi.la/post/6/80/8012806.json')
])
def test_generates_valid_post_address(post_id: int, expected: str):
    assert create_post_filepath(post_id) == expected
