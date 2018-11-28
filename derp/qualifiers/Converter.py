from .QualifierTree import *
import derp.criteria

ROUGHLY_INTERVAL_PERCENTAGE = 0.1

class LarkQualifierConverter:
    @staticmethod
    def convert(root_qualifier):
        """
        Converts a Lark AST for a qualifier to a QualifierTree
        :param root_qualifier: a Lark AST representing a set of qualifiers for a single expression
        :return: a QualifierTree representing the set of qualifiers
        """

        # We need to use a top down visitor in order to construct the tree
        # Lark does not provide a top down visitor

        switch_cases = {
            "qualifier_and": LarkQualifierConverter.__and,
            "qualifier_or": LarkQualifierConverter.__or,
            "match_qualifier": LarkQualifierConverter.__matching,
            "number_qualifier": LarkQualifierConverter.__number_check,
            "substring_qualifier": LarkQualifierConverter.__substring_check,
            "boolean_qualifier": LarkQualifierConverter.__boolean_check,
            "about_qualifier": LarkQualifierConverter.__about_check,
            "string_qualifier": LarkQualifierConverter.__string_check,
            "date_qualifier": LarkQualifierConverter.__date_check
        }
        default_case = lambda qualifier_node: print("Default Case:\n" + qualifier_node.pretty())

        if root_qualifier.data in switch_cases:
            return switch_cases[root_qualifier.data](root_qualifier)
        else:
            default_case(root_qualifier)
            assert False

    @staticmethod
    def __and(qualifier_node):
        return AndNode(
            LarkQualifierConverter.convert(qualifier_node.children[0]),
            LarkQualifierConverter.convert(qualifier_node.children[1])
        )

    @staticmethod
    def __or(qualifier_node):
        return OrNode(
            LarkQualifierConverter.convert(qualifier_node.children[0]),
            LarkQualifierConverter.convert(qualifier_node.children[1])
        )

    @staticmethod
    def __matching(qualifier_node):
        inner_criteria = derp.criteria.Criteria(qualifier_node.children[0])
        negate = qualifier_node.children[1]
        ret_node = inner_criteria.qualifier_tree()

        # Check the negate flag
        if negate:
            ret_node = NotNode(ret_node)
        return ret_node

    @staticmethod
    def __number_check(qualifier_node):
        field = qualifier_node.children[0]
        check_type = qualifier_node.children[1]
        number = qualifier_node.children[2]
        if check_type == "<":
            return UnderNumberCheck(field, number)
        elif check_type == ">":
            return OverNumberCheck(field, number)
        elif check_type == "<=":
            return NotNode(OverNumberCheck(field, number))
        elif check_type == ">=":
            return NotNode(UnderNumberCheck(field, number))
        elif check_type == "=":
            return ExactNumberCheck(field, number)
        elif check_type == "!=":
            return NotNode(ExactNumberCheck(field, number))
        elif check_type == "~":
            return AndNode(
                OverNumberCheck(field, number - ROUGHLY_INTERVAL_PERCENTAGE * number),
                UnderNumberCheck(field, number + ROUGHLY_INTERVAL_PERCENTAGE * number)
            )
        elif check_type == "!~":
            return NotNode(AndNode(
                OverNumberCheck(field, number - ROUGHLY_INTERVAL_PERCENTAGE * number),
                UnderNumberCheck(field, number + ROUGHLY_INTERVAL_PERCENTAGE * number)
            ))
        else:
            assert False

    @staticmethod
    def __substring_check(qualifier_node):
        field = qualifier_node.children[0]
        substring = qualifier_node.children[1]
        negate = qualifier_node.children[2]

        ret_node = SubstringCheck(field, substring)
        if negate:
            ret_node = NotNode(ret_node)
        return ret_node

    @staticmethod
    def __boolean_check(qualifier_node):
        field = qualifier_node.children[0]
        negate = qualifier_node.children[1]

        return BooleanCheck(field, negate)

    @staticmethod
    def __about_check(qualifier_node):
        topic = qualifier_node.children[0]
        negate = qualifier_node.children[1]

        ret_node = AboutCheck(topic)
        if negate:
            ret_node = NotNode(ret_node)
        return ret_node

    @staticmethod
    def __string_check(qualifier_node):
        string = qualifier_node.children[0]
        field = qualifier_node.children[1]
        negate = qualifier_node.children[2]

        ret_node = StringCheck(field, string)

        if negate:
            ret_node = NotNode(ret_node)

        return ret_node

    @staticmethod
    def __date_check(qualifier_node):
        field = qualifier_node.children[0]
        check_type = qualifier_node.children[1]
        date = qualifier_node.children[2]

        if check_type == "=":
            return DateOnCheck(field, date)
        elif check_type == ">":
            return DateAfterCheck(field, date)
        elif check_type == "<":
            return DateBeforeCheck(field, date)
        else:
            assert False