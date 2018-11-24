from .semantic_checkers import *


class SemanticChecker():
    def __init__(self, get_loaded_fields, is_criteria, is_selection, module_exists, module_loaded,
                 any_modules_loaded, is_selection_mode, buffer_size):
        """
        :param get_loaded_fields: function to get fields provided by loaded modules on a per-module basis. Returns tuple(tuple(str))
        :param is_criteria: boolean function to check if a criteria exists
        :param is_selection: boolean function to check if a selection exists
        :param module_exists: boolean function to check if a module exists, loaded or unloaded
        :param module_loaded: boolean function to check if a module is loaded
        :param any_modules_loaded: boolean function to check if at least 1 module is loaded
        :param is_selection_mode: boolean function to check if current parse mode is for creating selections
        :param buffer_size: int function to get size of current create buffer
        """

        self.__visitors = [CheckCreateStatement(any_modules_loaded),
                           CheckLoadX(module_exists, module_loaded),
                           CheckReadX(is_selection),
                           CheckRecallOrClearX(is_criteria, is_selection),
                           CheckSaveNonEmpty(buffer_size, is_selection_mode),
                           CheckSaveX(is_criteria, is_selection,
                                      is_selection_mode),
                           CheckUnloadX(module_loaded)]

    def check(self, ast):
        """
        Performs semantic checks not implicitly done during the AST Transform

        * Main Mode
            * Recall X or Clear X but X does not exist
            * Read X but selection X does not exist
            * Load X but X doesn't exist
            * Load X but X is loaded
            * Unload X but X not loaded
            * Going to creation or selection mode with no modules loaded
        * Selection/Criteria Mode
            * Matching X but criteria X does not exist
            * Matching X but no modules are loaded to provide the fields used in X
            * Save as X but X already exists as other type
        """
        for visitor in self.__visitors:
            visitor.visit(ast)
