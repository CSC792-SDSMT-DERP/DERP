from .IFileManager_tests import *
from .MockFileManager import *


# Use class scope to keep all files created/destroyed
# by the tests persistent
@pytest.fixture(scope="class")
def filemanager_impl():
    return MockFileManager()
