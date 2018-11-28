from .ISessionStateController_tests import *
from .MockFileManager import *
from ..SessionStateController import *


# Use class scope to keep all files created/destroyed
# by the tests persistent
@pytest.fixture(scope="function")
def sessionstate_impl(request):
    fm = MockFileManager()

    return SessionStateController(fm)