from .IFileManager_tests import *
from ..FileManager import *

import pytest
import os
import shutil
import tempfile


# Use class scope to keep all files created/destroyed
# by the tests persistent
@pytest.fixture(scope="class")
def filemanager_impl(request):
    # Setup
    temp_dir = tempfile.mkdtemp()

    # Teardown
    def cleanup():
        shutil.rmtree(temp_dir)

    # Add teardown function
    request.addfinalizer(cleanup)

    # Return implementation
    return FileManager(temp_dir)


class TestFileManager:
    """
    Tests for file manager concrete type
    """

    def test_root_dir_must_exist(self):
        random_dir_name = ''
        while len(random_dir_name) == 0 or os.path.exists(random_dir_name):
            random_dir_name = ''.join(random.choice(
                string.ascii_letters) for _ in range(10))

        with pytest.raises(FileIOException):
            fm = FileManager(random_dir_name)

    # Test that file manager always uses an absolute file
    # path for its root dir
    def test_root_dir_is_always_absolute(self):
        temp_dir = tempfile.mkdtemp()

        fm1 = FileManager(os.path.relpath(temp_dir))
        fm2 = FileManager(temp_dir)

        assert(fm1.root_dir() == fm2.root_dir())
        assert(os.path.isabs(fm1.root_dir()))

        shutil.rmtree(temp_dir)

    # Test that files are created when writes happen
    def test_new_file_is_created(self, filemanager_impl):
        target_file = os.path.join(filemanager_impl.root_dir(), "tmpfile.txt")
        filemanager_impl.write_file("tmpfile.txt", ["single line of data"])

        assert(os.path.isfile(target_file))

    # Test that files are deleted when deletes happen
    def test_file_is_deleted(self, filemanager_impl):
        target_file = os.path.join(filemanager_impl.root_dir(), "tmpfile.txt")
        filemanager_impl.delete_file("tmpfile.txt")

        assert(not os.path.exists(target_file))

    # Test that full paths are created to files
    def test_path_is_created(self, filemanager_impl):
        target_path = os.path.join("tmpdir", "tmpfile.txt")
        target_file = os.path.join(filemanager_impl.root_dir(), target_path)

        filemanager_impl.write_file(target_path, ["single line of data"])

        assert(os.path.isfile(target_file))

    # Test that file accesses are not allowed outside the root dir
    def test_cant_work_above_root_dir(self, filemanager_impl):
        dir_above_root_absolute = os.path.abspath(
            os.path.join(filemanager_impl.root_dir(), ".."))

        dir_next_to_root_absolute = os.path.join(
            dir_above_root_absolute, "neighbor_dir")

        dirs_to_test = [dir_above_root_absolute,
                        dir_next_to_root_absolute, "..", os.path.join("..", "neighbor_dir")]
        files_to_test = [os.path.join(x, "tmpfile.txt") for x in dirs_to_test]

        for f in files_to_test:
            got_exception = False
            try:
                filemanager_impl.write_file(f, ["single line of data"])
            except FileIOException as e:
                got_exception = True
                assert(e.get_reason() == FileIOException.Reason.SECURITY)

            assert(got_exception)

        for f in files_to_test:
            got_exception = False
            try:
                filemanager_impl.read_file(f)
            except FileIOException as e:
                got_exception = True
                assert(e.get_reason() == FileIOException.Reason.SECURITY)

            assert(got_exception)

        for f in files_to_test:
            got_exception = False
            try:
                filemanager_impl.delete_file(f)
            except FileIOException as e:
                got_exception = True
                assert(e.get_reason() == FileIOException.Reason.SECURITY)

            assert(got_exception)
