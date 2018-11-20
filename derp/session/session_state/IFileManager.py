"""
IFileManager.py

Interface definition for FileManager objects.
"""


class IFileManager:
    """
    FileManagers must be able to read and write files at given paths.
    """

    def read_file(self, file_path):
        """
        Reads input from the specified file and returns a list of strings
        representing line separated input.
        :param file_path: path to the file to read from
        :raises FileIOException: raised if the FileManager failed to read the file
        """
        pass

    def write_file(self, file_path, lines):
        """
        Writes each line in lines to the specified file.
        :param file_path: path to the file to write to
        :param lines: lines to write to the file
        :raises FileIOException: raised if the FileManager failed to write the file
        """
        pass

    def delete_file(self, file_path):
        """
        Deletes the file at the specified path.
        :param file_path: path to the file to delete
        :raises FileIOException: raised if the FileManager failed to delete the file
        """
        pass
