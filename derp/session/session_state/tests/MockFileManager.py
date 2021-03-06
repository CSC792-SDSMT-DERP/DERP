from ..IFileManager import *
from derp.exceptions import FileIOException

import os


class MockFileManager(IFileManager):
    def __init__(self):
        self.__files = {}

    def _validate_path(self, path):
        path = os.path.realpath(path)

        return path

    def file_exists(self, file_path):
        return self._validate_path(file_path) in self.__files

    def read_file(self, file_path):
        path = self._validate_path(file_path)

        if path not in self.__files:
            raise FileIOException(
                file_path, FileIOException.OperationType.READ, FileIOException.Reason.FILE_SYSTEM)

        return self.__files[path]

    def write_file(self, file_path, lines):
        path = self._validate_path(file_path)

        self.__files[path] = list(filter(lambda x: len(x) > 0, lines))

    def delete_file(self, file_path):
        path = self._validate_path(file_path)

        if path not in self.__files:
            raise FileIOException(
                file_path, FileIOException.OperationType.DELETE, FileIOException.Reason.FILE_SYSTEM)

        del self.__files[path]
