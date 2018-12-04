from derp.qualifiers import *
from derp.exceptions import *


class ASTKey:
    """
    Allows us to hash Lark ASTs based on their string values
    """

    def __init__(self, ast):
        self.__ast = ast

    def ast(self):
        return self.__ast

    def __eq__(self, other):
        return str(self.__ast) == str(other.__ast)

    def __hash__(self):
        return hash(str(self.__ast))


class Selection:
    """
    Represents a selection using a list of SelectionExpressions.
    Builds SelectionExpressions from parsed selection statements.
    """

    def __init__(self, selection_ast_list=None):
        if selection_ast_list is None:
            selection_ast_list = []

        # mapping from the asts referenced in the selection to the qualifier
        # trees needing to be executed for each source ast.
        # Key: str(source_ast) Value: (source_ast, qualifier_tree)
        # The ast must be stringified to use it as a dict key
        self.__source_ast_qualifier_tree_map = {}

        for ast in selection_ast_list:
            self.append(ast)

    def append(self, selection_ast):
        add_remove_expr = selection_ast.children[0]
        # Add expressions and remove expressions need different handlers
        if add_remove_expr.data == "add_expression":
            self.__append_add_expression(
                AddSelectionExpression(add_remove_expr.children[0]))
        else:
            self.__append_remove_expression(
                RemoveSelectionExpression(add_remove_expr.children[0]))

    def __append_add_expression(self, expression):
        # Add expressions may reference multiple module sources or selection sources
        for source_ast in expression.source_asts():
            if source_ast.data == "source_module":
                # Module sources are easy, we just or the qualifier tree for the
                # expression with the existing tree for that source
                source_ast_key = ASTKey(source_ast)

                if source_ast_key in self.__source_ast_qualifier_tree_map:
                    self.__source_ast_qualifier_tree_map[source_ast_key] = self.__insert_or(
                        self.__source_ast_qualifier_tree_map[source_ast_key],
                        expression.qualifier_tree()
                    )
                else:
                    self.__source_ast_qualifier_tree_map[source_ast_key] = expression.qualifier_tree(
                    )
            elif source_ast.data == "source_selection":
                # Selection sources are a bit more difficult.
                # We need to get the source ast - qualifier tree map for the referenced
                # selection, qualify each qualifier tree for each nested source with the
                # qualifier tree specified in this expression and or each nested source's
                # qualifier tree with the one in this selection's map
                nested_selection = Selection(source_ast.children[0])
                nested_source_ast_qualifier_tree_map = nested_selection.source_ast_qualifier_tree_map()
                for nested_source_ast_key in nested_source_ast_qualifier_tree_map:
                    if nested_source_ast_key in self.__source_ast_qualifier_tree_map:
                        self.__source_ast_qualifier_tree_map[nested_source_ast_key] = self.__insert_or(
                            self.__source_ast_qualifier_tree_map[nested_source_ast_key],
                            self.__insert_and(
                                nested_source_ast_qualifier_tree_map[nested_source_ast_key],
                                expression.qualifier_tree()
                            )
                        )
                    else:
                        self.__source_ast_qualifier_tree_map[nested_source_ast_key] = self.__insert_and(
                            nested_source_ast_qualifier_tree_map[nested_source_ast_key],
                            expression.qualifier_tree()
                        )

    def __append_remove_expression(self, expression):
        if len(self.__source_ast_qualifier_tree_map) == 0:
            raise NoPostsAddedSException(
                "Posts must be added before they may be removed from a selection")

        for source_ast_key, source_qualifier_tree in self.__source_ast_qualifier_tree_map.items():
            # each source must already have a corresponding tree
            # as REMOVE statements may only come after at least one
            # ADD statement
            self.__source_ast_qualifier_tree_map[source_ast_key] = self.__insert_and(
                self.__source_ast_qualifier_tree_map[source_ast_key],
                NotNode(expression.qualifier_tree())
            )

    @staticmethod
    def __insert_and(tree1, tree2):
        """
        Helper to remove None checks as Add statements without qualifiers produce None trees.
        """
        if tree1 is None:
            return tree2
        elif tree2 is None:
            return tree1
        else:
            return AndNode(tree1, tree2)

    @staticmethod
    def __insert_or(tree1, tree2):
        """
        Helper to remove None checks as Add statements without qualifiers produce None trees.
        """
        if tree1 is None:
            return tree2
        elif tree2 is None:
            return tree1
        else:
            return OrNode(tree1, tree2)

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

        if len(selector.children) > 1:
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
