"""
Transformer.py
Implementation for Transformer objects.
"""

from derp.language.ITransformer import ITransformer
from derp.exceptions.exceptions import SemanticException

from lark import Transformer as LarkTransformer, Visitor as LarkVisitor
from lark import v_args

from datetime import date
from datetime import timedelta
from calendar import monthrange

# Map month names to which month number they are
MONTH_NAME_TO_INDEX = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}


class Transformer(ITransformer):
    """
    Defines the transform function which performs semantic analysis and macro expansion on an AST
    as provided by an IParser.
    """

    def transform(self, ast):
        """
        Performs semantic analysis on the input tree and macro expansion.
        Returns the transformed AST if the input is semantically correct.
        May raise derp.exceptions.SemanticException.
        :param ast: a parse tree as created by an IParser
        :return: A transformed, semantically valid AST
        """

        class DateCheckTransformer(LarkTransformer):
            """
            Find date check expressions and evaluate the date contained
            """

            def date(self, children):
                """
                Convert DAY, MONTH, YEAR tokens to
                3-list of 2-lists, year, month, day and whether or not
                they were actually parsed
                """
                day = None
                month = None
                year = None

                month_str = ""

                assert(len(children) != 0)

                for tok in children:
                    if tok.type == "DAY":
                        day = eval(tok)
                    elif tok.type == "MONTH":
                        month_str = tok.lower()
                        assert(month_str in MONTH_NAME_TO_INDEX)
                        month = MONTH_NAME_TO_INDEX[month_str]
                    elif tok.type == "YEAR":
                        year = eval(tok)
                    else:
                        assert(False)

                assert(year is not None)

                # If both day and month parsed, make sure the day is a valid date
                if month is not None and day is not None:
                    last_valid_day = monthrange(year, month)[1]
                    if day == 0 or day > last_valid_day:
                        raise SemanticException(str(
                            day) + " is not a valid day of the month in " + month_str + " of " + str(year))

                return [[year, True],
                        [month or 1, month is not None],
                        [day or 1, day is not None]]

            @v_args(inline=True)
            def date_qualifier(self, with_exp, field, check_type, date_info):
                """
                Take a date check type and date information parsed
                and determine the actual date to check against
                """

                op = "="

                year = date_info[0][0]
                month = date_info[1][0]
                day = date_info[2][0]

                year_found = date_info[0][1]
                month_found = date_info[1][1]
                day_found = date_info[2][1]

                assert(year_found)
                if check_type.type == "DATE_EXACT" and (not day_found or not month_found):
                    raise SemanticException(
                        "Exact date check requires month, day, and year all be specified")

                elif check_type.type == "DATE_BEFORE":
                    op = "<"

                    # If no month parsed, default to january
                    if not month_found:
                        month = 1

                    # If no day parsed, default to the first
                    if not day_found:
                        day = 1

                elif check_type.type == "DATE_AFTER":
                    op = ">"

                    # If no month parsed, default to December
                    if not month_found:
                        month = 12

                    # If no day parsed, default to last day of month
                    if not day_found:
                        day = monthrange(year, month)[1]

                target_date = None
                try:
                    target_date = date(year, month, day)
                except Exception as e:
                    raise SemanticException(
                        "Unable to create date type from " + str(month) + "/" + str(day) + "/" + str(year) + ": " + e.args[0]) from e

                if with_exp.lower() == "without":
                    if check_type.type == "DATE_AFTER":
                        op = "<"
                        target_date = target_date + timedelta(hours=24)
                    elif check_type.type == "DATE_BEFORE":
                        op = ">"
                        target_date = target_date - timedelta(hours=24)

                return [field, op, target_date]

        dct = DateCheckTransformer()
        ast = dct.transform(ast)

        return ast
