class IOException (Exception):
    """ Indicates that reading or writing files failed"""
    pass


class TextParseException (Exception):
    """ Indicates that parsing using the Lark parser failed """
    pass


class GrammarMergeException (Exception):
    """ Indicates that merging two Grammars is not possible """
    pass


class GrammarDefinitionException (Exception):
    """ Indicates that creating a Grammar from a dictionary is not possible """
    pass


class SemanticException (Exception):
    """ Indicates that a processed AST is not semantically correct """
    pass


class ModuleDefinitionException(Exception):
    """ Indicates that a module was not able to be registered """
    pass


class ModuleRegistrationException(Exception):
    """ Indicates that a module was not able to be registered """
    pass


class ModuleNotRegisteredException(Exception):
    """ Indicates that a module was not registered when it was referenced """
    pass


class ModuleNotLoadedException(Exception):
    """ Indicates that a module was not loaded when it was referenced """
    pass
