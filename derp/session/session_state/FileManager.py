"""
FileManager.py

Class definition for the FileManager object.
"""
import io
import os
from pathlib import Path

from .IFileManager import IFileManager

from derp.exceptions import FileIOException


class FileManager(IFileManager):
    """
    The FileManager reads and writes persisted selections and criteria.
    """

    def __init__(self, root_dir=os.getcwd()):
        if not os.path.exists(root_dir):
            raise FileIOException(
                root_dir, FileIOException.OperationType.READ, FileIOException.Reason.FILE_SYSTEM)

        self.__working_directory = os.path.realpath(root_dir)

    def root_dir(self):
        return self.__working_directory

    def __target_file_path(self, file_path):
        working_directory = self.__working_directory

        target_file = os.path.join(
            working_directory, file_path) if not os.path.isabs(file_path) else file_path
        real_target_file = os.path.realpath(target_file)

        return real_target_file

    def file_exists(self, file_path):
        working_directory = self.__working_directory
        target_file = self.__target_file_path(file_path)

        if not target_file.startswith(working_directory):
            raise FileIOException(
                file_path, FileIOException.OperationType.READ, FileIOException.Reason.SECURITY)

        return os.path.isfile(target_file)

    def read_file(self, file_path):
        """
        Reads input from the specified file and returns a list of strings
        representing line separated input. 
        Removes 1 newline from the end of each line
        :param file_path: path to the file to read from
        :raises FileIOException: raised if the FileManager failed to read the file or the path is above the manager's root dir
        """

        working_directory = self.__working_directory
        target_file = self.__target_file_path(file_path)

        if not target_file.startswith(working_directory):
            raise FileIOException(
                file_path, FileIOException.OperationType.READ, FileIOException.Reason.SECURITY)
        else:
            try:
                with io.open(target_file, "r") as file:
                    lines = file.readlines()

                    # Remove \n from lines, and remove empty lines
                    delimited_lines = list(filter(lambda l: len(
                        # Unsure why, but it seems like removing the \n is required only sometimes?
                        l) != 0, map(lambda s: str(s[0:-1]) if s.endswith('\n') else s, lines)))
                    return delimited_lines
            except IOError as e:
                raise FileIOException(target_file, FileIOException.OperationType.READ,
                                      FileIOException.Reason.FILE_SYSTEM) from e

    def write_file(self, file_path, lines):
        """
        Writes each non-empty line in lines to the specified file.
        Each line has a newline appended to it before writing
        :param file_path: path to the file to write to
        :param lines: lines to write to the file
        :raises FileIOException: raised if the FileManager failed to write the file or the path is above the manager's root dir
        """

        working_directory = self.__working_directory
        target_file = self.__target_file_path(file_path)

        if not target_file.startswith(working_directory):
            raise FileIOException(
                file_path, FileIOException.OperationType.WRITE, FileIOException.Reason.SECURITY)
        else:
            file_directory = os.path.dirname(target_file)
            Path(file_directory).mkdir(parents=True, exist_ok=True)

            try:
                delimited_lines = map(lambda x: str(x) + '\n', filter(lambda y: len(
                    y) != 0, lines))
                with io.open(target_file, "w") as file:
                    file.writelines(delimited_lines)
            except IOError as e:
                raise FileIOException(target_file, FileIOException.OperationType.WRITE,
                                      FileIOException.Reason.FILE_SYSTEM) from e

    def delete_file(self, file_path):
        """
        Deletes the file at the specified path.
        :param file_path: path to the file to delete
        :raises FileIOException: raised if the FileManager failed to delete the file or the path is above the manager's root dir
        """

        working_directory = self.__working_directory
        target_file = self.__target_file_path(file_path)

        if not target_file.startswith(working_directory):
            raise FileIOException(
                file_path, FileIOException.OperationType.DELETE, FileIOException.Reason.SECURITY)
        else:
            try:
                os.remove(target_file)
            except IOError as e:
                raise FileIOException(target_file, FileIOException.OperationType.DELETE,
                                      FileIOException.Reason.FILE_SYSTEM) from e
