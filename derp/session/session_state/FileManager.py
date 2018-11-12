"""
FileManager.py

Class definition for the FileManager object.
"""
import io
from derp.session.session_state.IFileManager import IFileManager


class FileManager(IFileManager):
    """
    The FileManager reads and writes persisted selections and criteria.
    """

    def __init__(self):
        pass

    def read_file(self, file_path):
        """
        Reads input from the specified file and returns a list of strings
        representing line separated input.
        :param file_path: path to the file to read from
        :raises IOException: raised if the FileManager failed to read the file
        """
        file = io.open(file_path, "r")
        lines = file.readlines()
        return lines

    def write_file(self, file_path, lines):
        """
        Writes each line in lines to the specified file.
        :raises IOException: raised if the FileManager failed to write the file
        """
        file = io.open(file_path, "w")
        file.writelines(lines)
