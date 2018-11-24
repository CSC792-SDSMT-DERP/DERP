import pytest

from . import execute_and_check_derp_statements
from derp.session import UXActionType


class TestMainModeBasicFunctionality:
    def test_main_mode_can_exit(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [("exit", UXActionType.EXIT)])

    def test_main_mode_can_stop(self, sessioncontroller_impl):
        execute_and_check_derp_statements(sessioncontroller_impl,
                                          [("stop", UXActionType.EXIT)])
