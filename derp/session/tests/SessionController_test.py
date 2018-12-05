from .targeted_tests.BasicFunctionality_tests import *
from .targeted_tests.SemanticCheck_tests import *
from .SessionControllerFactory import make as makeSessionController

import pytest


@pytest.fixture(scope="function")
def sessioncontroller_impl():
    return makeSessionController()
