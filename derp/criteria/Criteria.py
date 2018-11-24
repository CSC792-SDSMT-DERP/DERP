import derp.qualifiers


class Criteria:
    """
    Represents the set of qualifiers in a criteria.
    Eagerly computes the qualifier tree for a list of criteria expressions.
    """

    def __init__(self, criteria_ast_list):
        self.expressions = []
        for statement in criteria_ast_list:
            add_remove_expr = statement.children[0]
            if add_remove_expr.data == "add_expression":
                self.expressions.append(AddCriteriaExpression(add_remove_expr.children[0]))
            else:
                self.expressions.append(RemoveCriteriaExpression(add_remove_expr.children[0]))

        self.__set_qualifier_tree()

    def __set_qualifier_tree(self):
        """
        creates a qualifier tree representing the entire selection and stores it in self.__q_tree
        """

        # Insert an AndNode between two statements if the latter statement is a RemoveCriteriaExpression
        # and an OrNode otherwise.

        if isinstance(self.expressions[0], AddCriteriaExpression):
            ret_tree = self.expressions[0].qualifier_tree()
        else:
            ret_tree = derp.qualifiers.NotNode(self.expressions[0].qualifier_tree())

        for i in range(1, len(self.expressions)):
            curr_expression = self.expressions[i]

            if isinstance(curr_expression, AddCriteriaExpression):
                curr_tree = curr_expression.qualifier_tree()
            else:
                curr_tree = derp.qualifiers.NotNode(curr_expression.qualifier_tree())

            if isinstance(curr_expression, RemoveCriteriaExpression):
                ret_tree = derp.qualifiers.AndNode(ret_tree, curr_tree)
            else:
                ret_tree = derp.qualifiers.OrNode(ret_tree, curr_tree)

        self.__q_tree = ret_tree

    def qualifier_tree(self):
        return self.__q_tree


class CriteriaExpression:
    """
    Represents a set of qualifiers specified in a criteria expression.
    Eagerly computes the corresponding qualifier tree.
    """

    def __init__(self, selector):
        root_qualifier = selector.children[0]
        self.__q_tree = derp.qualifiers.LarkQualifierConverter.convert(root_qualifier)

    def qualifier_tree(self):
        return self.__q_tree


class AddCriteriaExpression(CriteriaExpression):
    pass


class RemoveCriteriaExpression(CriteriaExpression):
    pass