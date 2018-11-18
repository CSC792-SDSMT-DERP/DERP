from lark import Transformer, v_args
from lark import Tree


class StringQualifierReducer(Transformer):
    """
    Find string check expressions and evaluate the data contained, converting
    the children to the list
    [ field, string, negated ]
    """
    @v_args(inline=True)
    def string_qualifier(self, with_exp, string, field):
        negate = with_exp.lower() == "without"

        return Tree("string_qualifier", (field, string, negate))
