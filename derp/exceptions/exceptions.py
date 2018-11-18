from enum import Enum


class DerpException(Exception):
    """ Base class of Derp exceptions """
    pass


class FileIOException(DerpException):
    """ Indicates that reading or writing files failed"""

    def __init__(self, path, operation, reason):
        """
        Create a new FileIOException with the path, the operation that failed, and the reason.
        :param path: path that was involved in the IO operation
        :param operation: type of IO operation
        :param reason: reason for failure
        """
        self.__path = path
        self.__operation = operation
        self.__reason = reason

    def get_path(self):
        """return the path that was involved in the IO operation"""
        return self.__path

    def get_operation(self):
        """return the type of IO operation that was being performed"""
        return self.__operation

    def get_reason(self):
        """return the reason for the failure"""
        return self.__reason

    class OperationType(Enum):
        """
        Enumeration of possible IO operations
        """
        READ = 0
        WRITE = 1
        DELETE = 2

    class Reason(Enum):
        """
        Enumeration of possible reasons for failure
        """
        SECURITY = 0
        FILE_SYSTEM = 1


class TextParseException(DerpException):
    """ Indicates that parsing using the Lark parser failed """
    pass


class GrammarMergeException(DerpException):
    """ Indicates that merging two Grammars is not possible """
    pass


class GrammarDefinitionException(DerpException):
    """ Indicates that creating a Grammar from a dictionary is not possible """
    pass


class SemanticException(DerpException):
    """ Indicates that a processed AST is not semantically correct """
    pass


class ModuleDefinitionException(DerpException):
    """ Indicates that a module was not able to be registered """
    pass


class ModuleRegistrationException(DerpException):
    """ Indicates that a module was not able to be registered """
    pass


class ModuleNotRegisteredException(DerpException):
    """ Indicates that a module was not registered when it was referenced """
    pass


class ModuleNotLoadedException(DerpException):
    """ Indicates that a module was not loaded when it was referenced """
    pass
