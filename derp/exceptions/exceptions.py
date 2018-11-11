

class TextParseException (Exception):
    """ Indicates that parsing using the Lark parser failed """
    pass


class GrammarMergeException (Exception):
    """ Indicates that merging two Grammars is not possible """
    pass


class GrammarDefinitionException (Exception):
    """ Indicates that creating a Grammar from a dictionary is not possible """
    pass
