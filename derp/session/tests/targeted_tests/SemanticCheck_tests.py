import pytest

from . import execute_and_check_derp_statements

from derp.session import UXActionType, UXActionModeType
from derp.exceptions import *


@pytest.mark.slow
class TestMainModeSemanticChecks:

    @pytest.mark.parametrize("keyword", ["load", "unload", "read", "recall", "clear"])
    @pytest.mark.parametrize("id_string", [""])
    def test_empty_string_literals(self, id_string, keyword, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('{0} "{1}"'.format(keyword, id_string),
             UXActionType.ERROR, EmptyStringLiteralSException)
        ])

    @pytest.mark.parametrize("keyword", ["load"])
    @pytest.mark.parametrize("id_string", ["fake missing module"])
    def test_load_missing_module(self, id_string, keyword, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('{0} "{1}"'.format(keyword, id_string),
             UXActionType.ERROR, MissingModuleSException)
        ])

    @pytest.mark.parametrize("keyword", ["unload"])
    @pytest.mark.parametrize("id_string", ["fake missing module"])
    def test_unload_not_loaded_module(self, id_string, keyword, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('{0} "{1}"'.format(keyword, id_string),
             UXActionType.ERROR, ModuleNotLoadedSException)])

    def test_cant_load_module_twice(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "MockModule"', UXActionType.NO_OP,),
            ('load "MockModule"', UXActionType.ERROR, ModuleAlreadyLoadedSException)
        ])

    def test_cant_read_criteria(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "MockModule"', UXActionType.NO_OP,),
            ('create a new criteria', UXActionType.CHANGE_MODE,),
            ('add posts with "hello world" in the title', UXActionType.NO_OP,),
            ('save as "my criteria"', UXActionType.NO_OP,),
            ('stop', UXActionType.CHANGE_MODE,),
            ('read "my criteria"', UXActionType.ERROR, MissingSelectionSException)
        ])

    @pytest.mark.parametrize("keyword", ["read"])
    @pytest.mark.parametrize("id_string", ["fake missing id"])
    def test_read_missing_selection(self, id_string, keyword, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('{0} "{1}"'.format(keyword, id_string),
             UXActionType.ERROR, MissingSelectionSException)
        ])

    @pytest.mark.parametrize("create_type", ["criteria", "selection"])
    def test_cant_switch_mode_with_no_modules(self, create_type, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('create a new {0}'.format(create_type),
             UXActionType.ERROR, NoLoadedModulesSException)
        ])

    @pytest.mark.parametrize("keyword", ["recall", "clear"])
    @pytest.mark.parametrize("id_string", ["fake missing id"])
    def test_recall_and_clear_checks(self, id_string, keyword, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('{0} "{1}"'.format(keyword, id_string),
             UXActionType.ERROR, MissingIdSException)
        ])


@pytest.mark.slow
class TestCriteriaAndSelectionModeSemanticChecks:
    @pytest.mark.parametrize("create_type,from_expr", [('criteria', ''), ('selection', 'from mock')])
    def test_save_as_empty_name(self, create_type, from_expr, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new {0}'.format(create_type),
             UXActionType.CHANGE_MODE,),
            ('add posts {0} with "hello world" in the title'.format(
                from_expr), UXActionType.NO_OP,),
            ('save as ""', UXActionType.ERROR, EmptyStringLiteralSException,)
        ])

    def test_save_selection_as_criteria(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new criteria', UXActionType.CHANGE_MODE,),
            ('add posts with "hello world" in the title', UXActionType.NO_OP,),
            ('save as "mycriteria"', UXActionType.NO_OP,),
            ('stop', UXActionType.CHANGE_MODE,),

            ('create a new selection', UXActionType.CHANGE_MODE,),
            ('add posts from mock with "hello world" in the title', UXActionType.NO_OP,),
            ('save as "mycriteria"', UXActionType.ERROR,
             SaveSelectionAsCriteriaSException,),
        ])

    def test_save_criteria_as_selection(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new selection', UXActionType.CHANGE_MODE,),
            ('add posts from mock with "hello world" in the title', UXActionType.NO_OP,),
            ('save as "myselection"', UXActionType.NO_OP,),
            ('stop', UXActionType.CHANGE_MODE,),

            ('create a new criteria', UXActionType.CHANGE_MODE,),
            ('add posts with "hello world" in the title', UXActionType.NO_OP,),
            ('save as "myselection"', UXActionType.ERROR,
             SaveCriteriaAsSelectionSException,),
        ])

    @pytest.mark.parametrize("create_type", ['criteria', 'selection'])
    def test_save_empty_buffer(self, create_type, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new {0}'.format(create_type),
             UXActionType.CHANGE_MODE,),
            ('save as "mything"', UXActionType.ERROR,
             EmptySelectionOrCriteriaSException,),
        ])

    def test_cant_remove_before_add_selection(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new selection', UXActionType.CHANGE_MODE,),
            ('remove posts with "hello world" in the title',
             UXActionType.ERROR, NoPostsAddedSException,),
        ])

    def test_can_remove_before_add_criteria(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new criteria', UXActionType.CHANGE_MODE,),
            ('remove posts with "hello world" in the title',
             UXActionType.NO_OP,),
        ])

    def test_add_from_missing_selection(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new selection', UXActionType.CHANGE_MODE,),
            ('add posts from "myselection"',
             UXActionType.ERROR, MissingSelectionSException,),
        ])


@pytest.mark.slow
class TestQualifierSemanticChecks:

    @pytest.mark.parametrize("qualifier", ['with "" in the title', 'with the exact title ""', 'about ""', 'matching ""'])
    @pytest.mark.parametrize("create_type,from_expr", [('criteria', ''), ('selection', 'from mock')])
    def test_empty_string_literals(self, create_type, from_expr, qualifier, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new {0}'.format(create_type),
             UXActionType.CHANGE_MODE,),
            ('add posts {0} {1}'.format(from_expr, qualifier),
             UXActionType.ERROR, EmptyStringLiteralSException,),
        ])

    @pytest.mark.parametrize("qualifier", ['with the post date on 2018', 'with the post date on November 2018'])
    @pytest.mark.parametrize("create_type,from_expr", [('criteria', ''), ('selection', 'from mock')])
    def test_exact_date_check(self, create_type, from_expr, qualifier, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new {0}'.format(create_type),
             UXActionType.CHANGE_MODE,),
            ('add posts {0} {1}'.format(from_expr, qualifier),
             UXActionType.ERROR, MissingExactDateSException,),
        ])

    @pytest.mark.parametrize("qualifier", ['with the post date after 0', 'with the post date on November 32 2018', 'with the post date on August 0 2018'])
    @pytest.mark.parametrize("create_type,from_expr", [('criteria', ''), ('selection', 'from mock')])
    def test_invalid_date_check(self, create_type, from_expr, qualifier, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new {0}'.format(create_type),
             UXActionType.CHANGE_MODE,),
            ('add posts {0} {1}'.format(from_expr, qualifier),
             UXActionType.ERROR, InvalidDateSException,),
        ])

    @pytest.mark.parametrize("create_type,from_expr", [('criteria', ''), ('selection', 'from mock')])
    def test_matching_missing_criteria(self, create_type, from_expr, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl, [
            ('load "mockmodule"', UXActionType.NO_OP,),
            ('create a new {0}'.format(create_type),
             UXActionType.CHANGE_MODE,),
            ('add posts {0} matching "fake criteria"'.format(from_expr),
             UXActionType.ERROR, MissingCriteriaSException,),
        ])
