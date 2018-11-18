class DerpException(Exception):
    """ Base class of Derp exceptions """
    pass


class IOException (DerpException):
    """ Indicates that reading or writing files failed"""
    pass


class TextParseException (DerpException):
    """ Indicates that parsing using the Lark parser failed """
    pass


class GrammarMergeException (DerpException):
    """ Indicates that merging two Grammars is not possible """
    pass


class GrammarDefinitionException (DerpException):
    """ Indicates that creating a Grammar from a dictionary is not possible """
    pass


class SemanticException (DerpException):
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
