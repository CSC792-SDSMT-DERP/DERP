"""
Buffer.py

Class definition for the Buffer object
"""


class Buffer:
    """
    Buffer of commands that represent a single selection or criterion.
    """

    def __init__(self):
        self.__buffer = []

    def add_command(self, command):
        self.__buffer.append(command)

    def get_commands(self):
        return self.__buffer.copy()

    def clear(self):
        self.__buffer.clear()
