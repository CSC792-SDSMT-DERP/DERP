from derp.modules.tests import *

from .. import RedditModule

import json


@pytest.fixture(scope="function")
def module_impl():
    reddit_creds_json = open("reddit_credentials.json", "r")
    reddit_creds = json.load(reddit_creds_json)

    reddit_module = RedditModule(**reddit_creds)

    return reddit_module


@pytest.fixture(scope="function", params=['reddit', 'subreddit "news"'])
def module_source_string(request):
    return request.param
