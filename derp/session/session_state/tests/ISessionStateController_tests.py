import pytest

from derp.session.session_state.Buffer import *


@pytest.mark.parallel
class TestISessionStateController:
    """
    Class containing tests for the ISessionStateController interface
    Test file should
    * Import this object (from ISessionStateController_tests import TestISessionStateController)
    * Implement the sessionstate_impl pytest fixture to return the session state controller implementation
    * Tests require that no saved data exists from in the state controller when tests start

    The rest of the functionality of this interface is tested through the exhaustive integration tests
    """

    def test_can_switch_to_main_mode(self, sessionstate_impl):
        sessionstate_impl.disable_buffer()

    def test_can_switch_to_selection_mode(self, sessionstate_impl):
        sessionstate_impl.set_buffer_to_new_selection_buffer()

    def test_can_switch_to_criteria_mode(self, sessionstate_impl):
        sessionstate_impl.set_buffer_to_new_criteria_buffer()

    def test_returns_none_buffer_in_main_mode(self, sessionstate_impl):
        sessionstate_impl.disable_buffer()
        assert sessionstate_impl.get_buffer() is None

    def test_returns_selection_buffer_in_selection_mode(self, sessionstate_impl):
        sessionstate_impl.set_buffer_to_new_selection_buffer()
        assert isinstance(sessionstate_impl.get_buffer(), SelectionBuffer)

    def test_returns_criteria_buffer_in_criteria_mode(self, sessionstate_impl):
        sessionstate_impl.set_buffer_to_new_criteria_buffer()
        assert isinstance(sessionstate_impl.get_buffer(), CriterionBuffer)
