# python-nozomi
[![Build Status](https://travis-ci.com/Alfa-Q/python-nozomi.svg?token=NAcpuTjLC6CrUpWrqz9p&branch=master)](https://travis-ci.com/Alfa-Q/python-nozomi)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f3bffdff70794c5cb569645b60699e0b)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Alfa-Q/python-nozomi&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/python-nozomi.svg)](https://badge.fury.io/py/python-nozomi)
[![Python version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-green)](https://www.python.org/downloads/release/python-360/)

nozomi.la API in Python.

## Features
-   Retrieving image and video posts
-   Downloading posts

## Installation
```
$ pip install python-nozomi
```

## Example Usage
Retrieve and download a single post provided a URL
```python
from pathlib import Path
from nozomi import api

url = 'https://nozomi.la/post/26905532.html#veigar'

# Retrieve post metadata using the URL
post = api.get_post(url)

# Download the post
api.download_media(post, Path.cwd())
```

Retrieve and download all posts containing certain tags
```python   
# The tags that the posts retrieved must contain
positive_tags = ['veigar', 'wallpaper']

# Gets all posts with the tags 'veigar', 'wallpaper'
for post in api.get_posts(positive_tags):
    api.download_media(post, Path.cwd())
```

Retrieve all posts containing certain tags with blacklisted tags
```python
# The blacklisted tags
negative_tags = ['chogath']

# Gets all posts with the tags 'veigar', 'wallpaper' but no 'chogath' tag.
for post in api.get_posts(positive_tags, negative_tags):
    api.download_media(post, Path.cwd())
```
