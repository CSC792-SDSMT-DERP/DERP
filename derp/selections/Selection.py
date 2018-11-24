from derp.qualifiers import *

class Selection:
    """
    Represents a selection using a list of SelectionExpressions.
    Builds SelectionExpressions from a list of parsed selection statements.
    """
    def __init__(self, selection_ast_list):
        self.expressions = []
        for statement in selection_ast_list:
            add_remove_expr = statement.children[0]
            if add_remove_expr.data == "add_expression":
                self.expressions.append(AddSelectionExpression(add_remove_expr.children[0]))
            else:
                self.expressions.append(RemoveSelectionExpression(add_remove_expr.children[0]))


class SelectionExpression:
    """
    Represents the qualifiers contained in a SelectionExpression. Subclasses many provide
    additional data.
    """

    def qualifier_tree(self):
        """
        :return: a qualifier tree representing the qualifiers specified in the expression
        """
        pass

class AddSelectionExpression(SelectionExpression):
    """
    Represents an add selection expression using a list of source asts and a qualifier tree.
    """

    def __init__(self, selector):
        self.__source_asts = []
        source_node = selector.children[0]
        # TODO: Update the method of obtaining the source asts if a new transformer is put in place
        self.__source_asts = source_node.children

        root_qualifier = selector.children[1]
        self.__q_tree = LarkQualifierConverter.convert(root_qualifier)


    def source_asts(self):
        """
        :return: list of the asts for the sources specified in the selection expression
        """
        return self.__source_asts

    def qualifier_tree(self):
        return self.__q_tree


class RemoveSelectionExpression(SelectionExpression):
    """
    Represents a remove selection expression using a qualifier tree.
    """

    def __init__(self, selector):
        root_qualifier = selector.children[0]
        self.__q_tree = LarkQualifierConverter.convert(root_qualifier)

    def qualifier_tree(self):
        return self.__q_tree
