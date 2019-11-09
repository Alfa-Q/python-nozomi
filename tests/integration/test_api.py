"""Test the functionality of the api functions."""

import os
from pathlib import Path

import pytest

from nozomi import api
from nozomi.data import Post


@pytest.mark.integration
@pytest.mark.parametrize('positive_tags', [
    (['akali', 'sakimichan']),
    (['veigar'])
])
def test_get_posts_positive_tags(positive_tags):
    for post in api.get_posts(positive_tags=positive_tags):
        assert isinstance(post, Post)


@pytest.mark.integration
@pytest.mark.parametrize('positive_tags', [
    (['akali', 'sakimichan']),
    (['veigar'])
])
def test_get_all_posts_postitive_tags(positive_tags):
    for post in api.get_all_posts(positive_tags=positive_tags):
        assert isinstance(post, Post)


@pytest.mark.integration
@pytest.mark.parametrize('positive_tags, negative_tags', [
    (['akali', 'sakimichan'], ['nudity'])
])
def test_get_posts_negative_tags(positive_tags, negative_tags):
    for post in api.get_posts(positive_tags=positive_tags, negative_tags=negative_tags):
        assert isinstance(post, Post)
        # Ensure that the post does not contain the negative tag.
        assert not any(tag.tag in negative_tags for tag in post.general)


@pytest.mark.integration
@pytest.mark.parametrize('positive_tags, negative_tags', [
    (['akali', 'sakimichan'], [])
])
def test_download_media(positive_tags, negative_tags):
    repeat = 10
    for post in api.get_posts(positive_tags=positive_tags, negative_tags=negative_tags):
        image_name = api.download_media(post, Path.cwd())
        os.remove(Path.cwd().joinpath(image_name))
        repeat -= 1
        if repeat == 0:
            break
