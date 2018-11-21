from lark import Transformer, v_args
from lark import Tree, Token

from derp.exceptions import *


class MatchingQualifierReducer(Transformer):
    """
    Find matching check expressions and evaluate the data contained, converting the
    node to the AST for the qualifiers of the criteria to be matched
    """
    class __AddRemoveReducer(Transformer):
        """
        Ignores statement and expression nodes in the parse tree, leaving only add_expression or remove_expression
        as the root node
        """

        def statement(self, children):
            assert len(children) == 1
            return children[0]

        def expression(self, children):
            assert len(children) == 1
            return children[0]

    def __init__(self, criteria_exists, load_criteria):
        self.__get_asts = load_criteria
        self.__criteria_exists = criteria_exists

    def match_qualifier(self, children):
        criteria_name = None
        negate = False

        for child in children:
            if child.type == "NEGATE":
                negate = True
            elif child.type == "STRING":
                criteria_name = child
            else:
                assert(False)

        assert(criteria_name is not None)

        if not self.__criteria_exists(criteria_name):
            raise SemanticException(
                "Criteria '" + criteria_name + "' does not exist")

        asts = None
        try:
            asts = self.__get_asts(criteria_name)
        except FileIOException as e:
            raise SemanticException("Unable to load '" + criteria_name + "' from disk") from e
        except TextParseException as e:
            raise SemanticException("Modules were loaded during creation of '" + criteria_name + "' which are no longer loaded") from e
        except SemanticException as e:
            raise
        # No other exceptions should happen
        except Exception as e:
            assert(False)

        assert(asts is not None)

        # Pull out the add_expression and remove_expression in each of the loaded asts
        reduced_asts = []
        t = self.__AddRemoveReducer()

        for ast in asts:
            reduced_asts.append(t.transform(ast))

        return Tree('match_qualifier', [reduced_asts, negate])
