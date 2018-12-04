import pytest

from . import execute_and_check_derp_statements

from derp.session import UXActionType, UXActionModeType
from derp.exceptions import *


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


class TestCriteriaAndSelectionModeSemanticChecks:
    pass
