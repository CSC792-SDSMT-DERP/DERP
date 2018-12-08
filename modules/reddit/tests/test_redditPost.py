from ..RedditPost import RedditPost
from ..RedditModule import RedditModule

from derp.posts.tests import *

from lark import Tree

import json
import pytest


@pytest.fixture(scope="class")
def post_impl():
    reddit_creds_json = open("reddit_credentials.json", "r")
    reddit_creds = json.load(reddit_creds_json)

    reddit_module = RedditModule(**reddit_creds)
    post = next(reddit_module.get_posts(Tree("reddit_source", []), None))

    return post