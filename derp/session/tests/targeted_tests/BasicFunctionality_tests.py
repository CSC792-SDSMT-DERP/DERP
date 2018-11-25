import pytest

from . import execute_and_check_derp_statements

from derp.session import UXActionType, UXActionModeType


class TestMainModeBasicFunctionality:
    @pytest.mark.parametrize("command", ["exit", "stop"])
    def test_main_mode_can_exit(self, command, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [(command, UXActionType.EXIT)])

    def test_main_mode_can_load_module(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"', UXActionType.NO_OP, None,)])

    def test_main_mode_can_unload_module(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           ('unload "MockModule"', UXActionType.NO_OP, None,)])

    @pytest.mark.parametrize("type", [("criteria", UXActionModeType.CRITERIA),
                                      ("selection", UXActionModeType.SELECTION)])
    @pytest.mark.parametrize("command", ["create ",
                                         "create a ",
                                         "create new ",
                                         "create a new "])
    def test_can_enter_criteria_creation(self, command, type, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [('load "MockModule"',),
                                           (command+type[0], UXActionType.CHANGE_MODE, type[1],)])
