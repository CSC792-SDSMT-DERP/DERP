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
                self.expressions.append(
                    AddSelectionExpression(add_remove_expr.children[0]))
            else:
                self.expressions.append(
                    RemoveSelectionExpression(add_remove_expr.children[0]))
        self.__set_source_ast_qualifier_tree_map()

    def __set_source_ast_qualifier_tree_map(self):
        """
        Creates a mapping from the asts referenced in the selection to the qualifier
        trees needing to be executed for each source ast.
        Sets the result on self.__source_ast_qualifier_tree_map.
        """
        self.__source_ast_qualifier_tree_map = {}

        # loop through all of the expressions in order to reduce the multiple expression
        # qualifier trees into one per source ast
        for expression in self.expressions:

            # Add expressions and remove expressions need different handlers
            if isinstance(expression, AddSelectionExpression):

                # Add expressions may reference multiple module sources or selection sources
                for source_ast in expression.source_asts():
                    if source_ast.data == "source_module":
                        # Module sources are easy, we just or the qualifier tree for the
                        # expression with the existing tree for that source
                        if source_ast in self.__source_ast_qualifier_tree_map:
                            self.__source_ast_qualifier_tree_map[source_ast] = OrNode(
                                self.__source_ast_qualifier_tree_map[source_ast],
                                expression.qualifier_tree()
                            )
                        else:
                            self.__source_ast_qualifier_tree_map[source_ast] = expression.qualifier_tree()
                    elif source_ast.data == "source_selection":
                        # Selection sources are a bit more difficult.
                        # We need to get the source ast - qualifier tree map for the referenced
                        # selection, qualify each qualifier tree for each nested source with the
                        # qualifier tree specified in this expression and or each nested source's
                        # qualifier tree with the one in this selection's map
                        nested_selection = Selection(source_ast.children[0])
                        nested_source_ast_qualifier_tree_map = nested_selection.source_ast_qualifier_tree_map()
                        # TODO: Check the validity of doing this
                        for nested_source_ast in nested_source_ast_qualifier_tree_map:
                            if nested_source_ast in self.__source_ast_qualifier_tree_map:
                                self.__source_ast_qualifier_tree_map[nested_source_ast] = OrNode(
                                    self.__source_ast_qualifier_tree_map[nested_source_ast],
                                    AndNode(
                                        nested_source_ast_qualifier_tree_map[nested_source_ast],
                                        expression.qualifier_tree()
                                    )
                                )
                            else:
                                self.__source_ast_qualifier_tree_map[nested_source_ast] = AndNode(
                                    nested_source_ast_qualifier_tree_map[nested_source_ast],
                                    expression.qualifier_tree()
                                )

            elif isinstance(expression, RemoveSelectionExpression):
                # NOTE: We could support "Remove from module_source" here
                for source_ast in self.__source_ast_qualifier_tree_map:
                    # each source must already have a corresponding tree
                    # as REMOVE statements may only come after at least one
                    # ADD statement
                    self.__source_ast_qualifier_tree_map[source_ast] = AndNode(
                        self.__source_ast_qualifier_tree_map[source_ast],
                        NotNode(expression.qualifier_tree())
                    )

    def source_ast_qualifier_tree_map(self):
        return self.__source_ast_qualifier_tree_map


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
        source_asts = [source_node]

        if source_node.data == "source_or":
            source_asts = source_node.children

        self.__source_asts = source_asts

        if len(selector.children) != 0:
            root_qualifier = selector.children[1]
            self.__q_tree = LarkQualifierConverter.convert(root_qualifier)
        else:
            self.__q_tree = None

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
