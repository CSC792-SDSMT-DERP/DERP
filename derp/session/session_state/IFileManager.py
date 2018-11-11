"""
IFileManager.py

Interface definition for FileManager objects.
"""


class IFileManager:
    def read_file(self, file_path):
        """
        Reads input from the specified file and returns a list of strings
        representing line separated input.
        :param file_path: path to the file to read from
        :raises IOException: raised if the FileManager failed to read the file
        """
        pass

    def write_file(self, file_path, lines):
        """
        Writes each line in lines to the specified file.
        :raises IOException: raised if the FileManager failed to write the file
        """
        pass
