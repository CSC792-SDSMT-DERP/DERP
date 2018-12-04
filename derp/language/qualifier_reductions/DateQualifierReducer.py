from lark import Transformer, v_args
from lark import Tree

from datetime import date, timedelta
from calendar import monthrange

from derp.exceptions import *

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


class DateQualifierReducer(Transformer):
    """
    Find date check expressions and evaluate the date contained, converting
    the children to the list
    [ field, op, date ]
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
                raise InvalidDateSException(str(
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
            raise MissingExactDateSException(
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
        except ValueError as e:
            raise InvalidDateSException(
                "Unable to create date type from " + str(month) + "/" + str(day) + "/" + str(year) + ": " + e.args[0]) from e

        if with_exp.lower() == "without":
            if check_type.type == "DATE_AFTER":
                op = "<"
                target_date = target_date + timedelta(hours=24)
            elif check_type.type == "DATE_BEFORE":
                op = ">"
                target_date = target_date - timedelta(hours=24)

        return Tree("date_qualifier", [field, op, target_date])
