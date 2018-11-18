from lark import Transformer, v_args
from lark import Tree


class SubstringQualifierReducer(Transformer):
    """
    Find substring check expressions and evaluate the data contained, converting
    the children to the list
    [ field, substring, negated ]
    """
    @v_args(inline=True)
    def substring_qualifier(self, with_exp, string, field):
        negate = with_exp.lower() == "without"

        return Tree("substring_qualifier", (field, string, negate))
