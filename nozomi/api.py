"""Web API functions."""

import logging
import struct
import shutil
from pathlib import Path
from typing import Iterable, List

import requests
from dacite import from_dict

from nozomi.data import Post
from nozomi.exceptions import InvalidTagFormat, InvalidUrlFormat
from nozomi.helpers import sanitize_tag, create_tag_filepath, create_post_filepath, parse_post_id
from nozomi import byte_for

_LOGGER = logging.getLogger(__name__)


def get_post(url: str) -> Post:
    """Retrieve a single post.

    Args:
        url: The URL of the post to retrieve.

    Returns:
        A post in JSON format if it exists.

    """
    _LOGGER.debug('Retrieving a post from URL "%s"', url)
    try:
        post_id = parse_post_id(url)
        post_url = create_post_filepath(post_id)
        post_data = requests.get(post_url).json()
        _LOGGER.debug(post_data)
        return from_dict(data_class=Post, data=post_data)
    except InvalidUrlFormat:
        raise
    except Exception as ex:
        _LOGGER.exception(ex)
        raise


def get_posts(positive_tags: List[str], negative_tags: List[str]=None) -> Iterable[Post]:
    """Retrieve all post data that contains and doesn't contain certain tags.

    Args:
        positive_tags: The tags that the posts retrieved must contain.
        negative_tags: Optional, blacklisted tags.

    Yields:
        A post in JSON format, which contains the positive tags and doesn't contain the negative
        tags.

    """
    if negative_tags is None:
        negative_tags = list()
    _LOGGER.debug('Retrieving posts with positive_tags=%s and negative_tags=%s',
                  str(positive_tags), str(negative_tags))
    try:
        positive_post_urls = _get_post_urls(positive_tags)
        negative_post_urls = _get_post_urls(negative_tags)
        relevant_post_urls = set(positive_post_urls) - set(negative_post_urls)
        for post_url in relevant_post_urls:
            post_data = requests.get(post_url).json()
            _LOGGER.debug(post_data)
            yield from_dict(data_class=Post, data=post_data)
    except InvalidTagFormat:
        raise
    except Exception as ex:
        _LOGGER.exception(ex)
        raise


def download_media(post: Post, filepath: Path) -> List[str]:
    """Download all media on a post and save it.

    Args:
        post: The post to download.
        filepath: The file directory to save the media. The directory will be created if it doesn't
            already exist.

    Returns:
        The names of the images downloaded.

    """
    images_downloaded = []
    filepath.mkdir(parents=True, exist_ok=True)
    for media_meta_data in post.imageurls:
        image_url = media_meta_data.imageurl
        image_name = image_url.split('/')[-1]
        image_filepath = filepath.joinpath(image_name)
        _download_media(image_url, image_filepath)
        images_downloaded.append(image_name)
    return images_downloaded


def _download_media(image_url: str, filepath: Path):
    """Download an image and save it.

    Args:
        image_url: The image URL.
        filepath: The file directory to save the media. The directory will be created if it doesn't
            already exist.

    """
    headers = {
        'Host': 'i.nozomi.la',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://nozomi.la/',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    with requests.get(image_url, stream=True, headers=headers) as r:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    _LOGGER.debug('Image downloaded %s', filepath)


def _get_post_urls(tags: List[str]) -> List[str]:
    """Retrieve the links to all of the posts that contain the tags.

    Args:
        tags: The tags that the posts must contain.

    Returns:
        A list of post urls that contain all of the specified tags.

    """
    if len(tags) == 0: return tags
    _LOGGER.debug('Retrieving all URLs that contain the tags %s', str(tags))
    sanitized_tags = [sanitize_tag(tag) for tag in tags]
    nozomi_urls  = [create_tag_filepath(sanitized_tag) for sanitized_tag in sanitized_tags]
    tag_post_ids = [_get_post_ids(nozomi_url) for nozomi_url in nozomi_urls]
    tag_post_ids = set.intersection(*map(set, tag_post_ids)) # Flatten list of tuples on intersection
    post_urls = [create_post_filepath(post_id) for post_id in tag_post_ids]
    _LOGGER.debug('Got %d post urls containing the tags %s', len(tags), str(tags))
    return post_urls


def _get_post_ids(tag_filepath_url: str) -> List[int]:
    post_ids = []
    """Retrieve the .nozomi data file.

    Args:
        tag_filepath_url: The URL to a tag's .nozomi file.

    Returns:
        A list containing all of the post IDs that contain the tag.

    """
    _LOGGER.debug('Getting post IDs from %s', tag_filepath_url)
    try:
        headers={
    'Host': 'n.nozomi.la',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://nozomi.la/',
    'Origin': 'https://nozomi.la',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
                            }
        response = requests.get(tag_filepath_url, headers=headers)
        _LOGGER.debug('RESPONSE: %s', response)
        total_ids = len(response.content) // 4  # divide by the size of uint
        _LOGGER.info('Unpacking .nozomi file... Expecting %d post ids.', total_ids)
        result = []
        byte_for.bt_for(response.content,result)
        _LOGGER.debug('Unpacked data... Got %d total post ids! %s', len(result), str(result))
    except Exception as ex:
        _LOGGER.exception(ex)
    return result
