"""
Buffer.py

Class definition for the CriterionBuffer and SelectionBuffer objects
"""

from derp.selections import Selection
from derp.criteria import Criteria
from .IBuffer import IBuffer


class CriterionBuffer(IBuffer):
    def __init__(self):
        self.__buffer = []
        self.__data = Criteria()

    def add_command(self, input_line, semantic_tree):
        self.__data.append(semantic_tree)
        self.__buffer.append(input_line)

    def get_commands(self):
        return self.__buffer.copy()

    def get_data(self):
        return self.__data

    def clear(self):
        self.__buffer.clear()
        self.__data = Criteria()


class SelectionBuffer(IBuffer):
    def __init__(self):
        self.__buffer = []
        self.__data = Selection()

    def add_command(self, input_line, semantic_tree):
        # Note that we may encounter an exception when building the selection
        # so we do the buffer append last
        self.__data.append(semantic_tree)
        self.__buffer.append(input_line)

    def get_commands(self):
        return self.__buffer.copy()

    def get_data(self):
        return self.__data

    def clear(self):
        self.__buffer.clear()
        self.__data = Selection()
