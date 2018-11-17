from lark import Transformer, v_args
from lark import Tree, Token


class MatchingQualifierReducer(Transformer):
    """
    Find matching check expressions and evaluate the data contained, converting the
    node to the AST for the qualifiers of the criteria to be matched
    """
    pass
