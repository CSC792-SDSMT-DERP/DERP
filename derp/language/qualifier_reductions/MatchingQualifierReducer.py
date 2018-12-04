from lark import Transformer, v_args
from lark import Tree, Token

from derp.exceptions import *


def get_subtitute_ast_list(acquire_asts, criteria_or_selection_name):
    asts = None
    try:
        asts = acquire_asts(criteria_or_selection_name)

    # Already checked that the item exists, so the only way this fails is a file read error
    except FileIOException as e:
        raise FailToLoadExistingSException("Unable to load '" + criteria_or_selection_name + "' from disk") from e

    # Text in file was semantically checked when it was saved, so this only happens if the set of valid fields
    # changes. (Or the file was modified after it was written or not written by interpreter)
    except TextParseException as e:
        raise FailToParseExistingSException("Unable to parse '" + criteria_or_selection_name + "': " + e.args[0]) from e

    # Should only happen if there is a 'matching' qualifier in the loaded criteria or selection, and it fails to parse
    # or if the criteria/selection substituted was not written by the interpreter
    except SemanticException as e:
        raise

    # Criteria or selection contains a circular reference
    except RecursionError as e:
        raise CircularReferenceSException("'" + criteria_or_selection_name + "' contains a circular reference") from e

    # No other exceptions should happen
    except Exception as e:
        assert False

    assert(asts is not None)

    return asts


class MatchingQualifierReducer(Transformer):
    """
    Find matching check expressions and evaluate the data contained, converting the
    node to the AST for the qualifiers of the criteria to be matched
    """

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
            raise MissingCriteriaSException(
                "Criteria '" + criteria_name + "' does not exist")

        asts = get_subtitute_ast_list(self.__get_asts, criteria_name)

        return Tree('match_qualifier', [asts, negate, criteria_name])
