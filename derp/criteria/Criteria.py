import derp.qualifiers


class Criteria:
    """
    Represents the set of qualifiers in a criteria.
    Eagerly computes the qualifier tree for a list of criteria expressions.
    """

    def __init__(self, criteria_ast_list=None):
        if criteria_ast_list is None:
            criteria_ast_list = []
        self.__q_tree = None
        for ast in criteria_ast_list:
            self.append(ast)

    def append(self, criteria_ast):
        """
        Builds the underlying qualifier tree based off of the current state and the given criteria_ast.
        Order matters when appending criteria asts to a given criteria.
        :param criteria_ast: A Lark criteria ast which has been semantically validated
        """
        add_remove_expression = criteria_ast.children[0]
        is_add_expression = add_remove_expression.data == "add_expression"  # Otherwise remove expression
        selector = add_remove_expression.children[0]
        root_qualifier = selector.children[0]
        expression_q_tree = derp.qualifiers.LarkQualifierConverter.convert(root_qualifier)

        # Start out the criteria if it is empty
        if self.__q_tree is None:
            if is_add_expression:
                self.__q_tree = expression_q_tree
            else:
                self.__q_tree = derp.qualifiers.NotNode(expression_q_tree)
            return

        if is_add_expression:
            self.__q_tree = derp.qualifiers.OrNode(self.__q_tree, expression_q_tree)

        else:
            self.__q_tree = derp.qualifiers.AndNode(
                self.__q_tree,
                derp.qualifiers.NotNode(expression_q_tree)
            )

    def qualifier_tree(self):
        """
        :return: a QualifierTree which represents the constraints of the Criteria
        """
        return self.__q_tree
