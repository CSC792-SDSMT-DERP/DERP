from derp.modules.tests import *

from .mock_module import MockModule

import json


@pytest.fixture(scope="function")
def module_impl():
    return MockModule()


@pytest.fixture(scope="function", params=['mock'])
def module_source_string(request):
    return request.param
