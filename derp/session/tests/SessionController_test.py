from .targeted_tests.BasicFunctionality_tests import *
from .targeted_tests.SemanticCheck_tests import *

from .monkey_tests.random_text_tests import *
from .monkey_tests.random_keyword_strings import *
from .monkey_tests.random_statements import *

from .SessionControllerFactory import make as makeSessionController

import pytest


@pytest.fixture(scope="function")
def sessioncontroller_impl():
    return makeSessionController()
