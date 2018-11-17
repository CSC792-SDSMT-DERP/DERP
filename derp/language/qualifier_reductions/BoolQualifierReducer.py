from lark import Transformer, v_args
from lark import Tree, Token


class BoolQualifierReducer(Transformer):
    """
    Find bool check expressions and evaluate the data contained, converting
    the children to the list
    [ field, desired_value ]
    """

    def boolean_qualifier(self, children):
        negate = False
        field = None

        for child in children:
            # Check should have at most a FIELD and NEGATE token
            assert(isinstance(child, Token))

            if child.type == 'FIELD':
                field = child
            elif child.type == 'NEGATE':
                negate = True
            else:
                assert(False)

        assert(field is not None)

        # If not negated, we want to match True, if negated we want to match False
        return Tree("boolean_qualifier", (field, not negate))
