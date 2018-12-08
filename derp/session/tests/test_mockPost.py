from .mock_module import *
from derp.posts.tests import *

import pytest
from datetime import date

@pytest.fixture
def post_impl():
    module = MockModule()

    return MockPost(module, date.today(), 42, "hello world", False)