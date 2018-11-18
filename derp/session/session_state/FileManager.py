"""
FileManager.py

Class definition for the FileManager object.
"""
import io
import os
from derp.session.session_state.IFileManager import IFileManager
from derp.exceptions.exceptions import FileIOException


class FileManager(IFileManager):
    """
    The FileManager reads and writes persisted selections and criteria.
    """

    def read_file(self, file_path):
        """
        Reads input from the specified file and returns a list of strings
        representing line separated input.
        :param file_path: path to the file to read from
        :raises FileIOException: raised if the FileManager failed to read the file or the path is above the CWD
        """
        working_directory = os.getcwd()
        if os.path.realpath(os.path.join(working_directory, file_path)).startswith(working_directory):
            raise FileIOException(file_path, FileIOException.OperationType.READ, FileIOException.Reason.SECURITY)
        else:
            try:
                with io.open(os.path.join(working_directory, file_path), "r") as file:
                    lines = file.readlines()
                    return lines
            except IOError as e:
                raise FileIOException(file_path, FileIOException.OperationType.READ,
                                      FileIOException.Reason.FILE_SYSTEM) from e

    def write_file(self, file_path, lines):
        """
        Writes each line in lines to the specified file.
        :param file_path: path to the file to write to
        :param lines: lines to write to the file
        :raises FileIOException: raised if the FileManager failed to write the file or the path is above the CWD
        """
        working_directory = os.getcwd()
        if os.path.realpath(os.path.join(working_directory, file_path)).startswith(working_directory):
            raise FileIOException(file_path, FileIOException.OperationType.WRITE, FileIOException.Reason.SECURITY)
        else:
            file_directory = os.path.dirname(os.path.join(working_directory, file_path))
            if not os.path.exists(file_directory):
                os.mkdir(file_directory)

            try:
                with io.open(os.path.join(working_directory, file_path), "w") as file:
                    file.writelines(lines)
            except IOError as e:
                raise FileIOException(file_path, FileIOException.OperationType.WRITE,
                                      FileIOException.Reason.FILE_SYSTEM) from e

    def delete_file(self, file_path):
        """
        Deletes the file at the specified path.
        :param file_path: path to the file to delete
        :raises FileIOException: raised if the FileManager failed to delete the file or the path is above the CWD
        """
        working_directory = os.getcwd()
        if os.path.realpath(os.path.join(working_directory, file_path)).startswith(working_directory):
            raise FileIOException(file_path, FileIOException.OperationType.DELETE, FileIOException.Reason.SECURITY)
        else:
            try:
                os.remove(os.path.join(working_directory, file_path))
            except IOError as e:
                raise FileIOException(file_path, FileIOException.OperationType.DELETE,
                                      FileIOException.Reason.FILE_SYSTEM) from e
