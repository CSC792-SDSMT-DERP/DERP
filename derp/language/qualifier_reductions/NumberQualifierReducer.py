from lark import Transformer, v_args
from lark import Tree

CHECK_TYPE_AND_NEGATE_TO_OP = {
    "number_above": {False: ">", True: "<="},
    "number_below": {False: "<", True: ">="},
    "number_exact": {False: "=", True: "!="},
    "number_approx": {False: "~", True: "!~"},
}


class NumberQualifierReducer(Transformer):
    """
    Find number check expressions and evaluate the data contained, converting
    the children to the list
    [ field, op, value ]
    """
    @v_args(inline=True)
    def number_qualifier(self, with_exp, check_type, number_tok, field):
        negate = with_exp.lower() == "without"
        value = eval(number_tok)
        op = CHECK_TYPE_AND_NEGATE_TO_OP[check_type.data][negate]

        return Tree("number_qualifier", (field, op, value))
