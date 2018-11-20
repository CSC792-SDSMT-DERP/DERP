import pytest
import string
import random
import os

from derp.exceptions import FileIOException


def _random_num(lower, upper):
    return random.choice(range(lower, upper))


def _random_str():
    return ''.join(random.choice(
        string.ascii_letters + string.digits + " ") for _ in range(_random_num(10, 20)))


def _random_path(max_len):
    path = _random_str()
    for i in range(max_len):
        path = os.path.join(path, _random_str())
    return path


class TestIFileManager:
    """
    Class containing tests for the IFileManager interface
    Test file should
    * Import this object (from IFileManager_tests import TestIFileManager)
    * Implement the filemanager_impl pytest fixture to return the filemanager implementation
        * This fixture decorator must indicate 'class' scope or higher, to keep the object persistent through all
          tests defined in this class
    * Tests require that no files exist (from the filemanager's perspective) when testing starts
    * Tests in this class must be run in order, as they rely on filemanager state persisting
    """

    # Generate random files and texts to test with
    def setup_class(self):

        # Generate a bunch of unique random files to work with, up to 4 directories deep
        random_files = set()
        for i in range(5):
            random_files = random_files.union(
                set([_random_path(i) for _ in range(5)]))

        random_files = list(random_files)

        # Generate random text to store in the files
        random_text_1 = [[_random_str() for i in range(
            _random_num(5, 10))] for _ in range(len(random_files))]

        random_text_2 = [[_random_str() for i in range(
            _random_num(5, 10))] for _ in range(len(random_files))]

        random_text_3 = [[_random_str() for i in range(
            _random_num(5, 10))] for _ in range(len(random_files))]

        # Merge the random files and random text lists into a set of tests
        self.__random_tests = [
            (random_files[i], random_text_1[i], random_text_2[i], random_text_3[i])]

    # Tests that exceptions are raised on read and delete errors
    def test_exception_on_read_fail(self, filemanager_impl):
        for case in self.__random_tests:
            with pytest.raises(FileIOException):
                filemanager_impl.read_file(case[0])

    def test_exception_on_delete_fail(self, filemanager_impl):
        for case in self.__random_tests:
            with pytest.raises(FileIOException):
                filemanager_impl.delete_file(case[0])

    # Test that files can be created without raising an exception
    def test_can_create_files(self, filemanager_impl):
        for case in self.__random_tests:
            filemanager_impl.write_file(case[0], case[1])

    # Test that files can be read without raising an exception
    def test_can_read_files(self, filemanager_impl):
        for case in self.__random_tests:
            filemanager_impl.read_file(case[0])

    # Test that file data persists when files were newly created
    def test_new_file_text_persists(self, filemanager_impl):
        for case in self.__random_tests:
            text = filemanager_impl.read_file(case[0])
            assert text == case[1]

    # Test that files can be written over without raising an exception
    def test_can_overwrite_files(self, filemanager_impl):
        for case in self.__random_tests:
            filemanager_impl.write_file(case[0], case[2])

    # Test that file data persists when files were newly created
    def test_overwrite_file_text_persists(self, filemanager_impl):
        for case in self.__random_tests:
            text = filemanager_impl.read_file(case[0])
            assert text == case[2]

    # Tests that files can be deleted without raising an exception
    def test_can_delete_file(self, filemanager_impl):
        for case in self.__random_tests:
            text = filemanager_impl.delete_file(case[0])

    # Tests that deleted files cannot be read
    def test_cannot_read_deleted_file(self, filemanager_impl):
        for case in self.__random_tests:
            with pytest.raises(FileIOException):
                filemanager_impl.read_file(case[0])

    # Test that files can be rewritten without raising an exception
    def test_can_rewrite_files(self, filemanager_impl):
        for case in self.__random_tests:
            filemanager_impl.write_file(case[0], case[3])

    # Test that file data persists when files were deleted then rewritten
    def test_rewrite_file_text_persists(self, filemanager_impl):
        for case in self.__random_tests:
            text = filemanager_impl.read_file(case[0])
            assert text == case[3]

    # Test that empty strings are not written to file
    def test_ignore_empty_strings_on_write(self, filemanager_impl):
        random_text = [_random_str() for i in range(
            _random_num(5, 10))]

        random_text_with_empty = random_text.copy()
        for i in range(10):
            random_text_with_empty.append("")

        random.shuffle(random_text_with_empty)

        filemanager_impl.write_file("tmp", random_text_with_empty)
        test_read = filemanager_impl.read_file("tmp")

        assert(set(random_text) == set(test_read))
