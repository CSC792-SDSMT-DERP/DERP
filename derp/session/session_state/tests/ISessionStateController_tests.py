import pytest
from .random_data import *

from derp.exceptions import FileIOException


class TestISessionStateController:
    """
    Class containing tests for the ISessionStateController interface
    Test file should
    * Import this object (from ISessionStateController_tests import TestISessionStateController)
    * Implement the sessionstate_impl pytest fixture to return the session state controller implementation
        * This fixture decorator must indicate 'class' scope or higher, to keep the object persistent through all
          tests defined in this class
    * Tests require that no saved data exists from in the state controller when tests start
    * Tests in this class must be run in order, as they rely on state persisting
    """

    def setup_class(self):

        # Generate a bunch of unique random selections and criteria to work with
        random_selection_names = [random_str() for _ in range(5)]

        random_criteria_names = list(filter(lambda x: x not in random_selection_names, [
            random_str() for _ in range(5)]))

        # Generate random text to store in the files
        random_text_1 = [[random_str() for i in range(
            random_num(5, 10))] for _ in range(10)]

        random_text_2 = [[random_str() for i in range(
            random_num(5, 10))] for _ in range(10)]

        random_text_3 = [[random_str() for i in range(
            random_num(5, 10))] for _ in range(10)]

        # Merge the random files and random text lists into a set of tests
        self._random_selections = [
            (random_selection_names[i], random_text_1[i], random_text_2[i], random_text_3[i]) for i in range(5)]

        self._random_criteria = [
            (random_criteria_names[i], random_text_1[i+5], random_text_2[i+5], random_text_3[i+5]) for i in range(len(random_criteria_names))]

    def _write_case_to_buffer(self, buffer, text):
        buffer.clear()
        for line in text:
            buffer.add_command(line)

    # Tests that working with missing criteria and selections raises an exception
    def test_error_load_missing_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            with pytest.raises(FileIOException):
                sessionstate_impl.load_criteria(case[0])

    def test_error_load_missing_selection(self, sessionstate_impl):
        for case in self._random_selections:
            with pytest.raises(FileIOException):
                sessionstate_impl.load_selection(case[0])

    def test_error_delete_missing_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            with pytest.raises(FileIOException):
                sessionstate_impl.delete_criteria(case[0])

    def test_error_delete_missing_selection(self, sessionstate_impl):
        for case in self._random_selections:
            with pytest.raises(FileIOException):
                sessionstate_impl.delete_selection(case[0])

    def test_selections_dont_exist_on_start(self, sessionstate_impl):
        for case in self._random_selections:
            assert not sessionstate_impl.selection_exists(case[0])

    def test_criteria_dont_exist_on_start(self, sessionstate_impl):
        for case in self._random_criteria:
            assert not sessionstate_impl.criteria_exists(case[0])

    # Tests that buffer does not copy in get_buffer()
    def test_buffer_persistent(self, sessionstate_impl):
        buffer1 = sessionstate_impl.get_buffer()
        buffer2 = sessionstate_impl.get_buffer()

        assert buffer1 is buffer2

    # Tests that criteria and selections can be saved
    def test_can_save_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            self._write_case_to_buffer(sessionstate_impl.get_buffer(), case[1])
            sessionstate_impl.save_criteria(case[0])

    def test_can_save_selection(self, sessionstate_impl):
        for case in self._random_selections:
            self._write_case_to_buffer(sessionstate_impl.get_buffer(), case[1])
            sessionstate_impl.save_selection(case[0])

    def test_selections_exist_after_creation(self, sessionstate_impl):
        for case in self._random_selections:
            assert sessionstate_impl.selection_exists(case[0])

    def test_criteria_exist_after_creation(self, sessionstate_impl):
        for case in self._random_criteria:
            assert sessionstate_impl.criteria_exists(case[0])

    # Tests that criteria and selections are distinct
    def test_cannot_load_criteria_as_selection(self, sessionstate_impl):
        for case in self._random_criteria:
            with pytest.raises(FileIOException):
                sessionstate_impl.load_selection(case[0])

    def test_cannot_load_selection_as_criteria(self, sessionstate_impl):
        for case in self._random_selections:
            with pytest.raises(FileIOException):
                sessionstate_impl.load_criteria(case[0])

    def test_cannot_delete_criteria_as_selection(self, sessionstate_impl):
        for case in self._random_criteria:
            with pytest.raises(FileIOException):
                sessionstate_impl.delete_selection(case[0])

    def test_cannot_delete_selection_as_criteria(self, sessionstate_impl):
        for case in self._random_selections:
            with pytest.raises(FileIOException):
                sessionstate_impl.delete_criteria(case[0])

    # Tests that saved selections and criteria can be re-loaded
    def test_can_load_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            sessionstate_impl.load_criteria(case[0])

    def test_can_load_selection(self, sessionstate_impl):
        for case in self._random_selections:
            sessionstate_impl.load_selection(case[0])

    # Tests that loaded data is not mutated
    def test_loaded_selection_is_unchanged(self, sessionstate_impl):
        for case in self._random_selections:
            lines = sessionstate_impl.load_selection(case[0])

            assert(lines == case[1])

    def test_loaded_criteria_is_unchanged(self, sessionstate_impl):
        for case in self._random_criteria:
            lines = sessionstate_impl.load_criteria(case[0])

            assert(lines == case[1])

    # Tests that data can be overwritten
    def test_can_overwrite_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            self._write_case_to_buffer(sessionstate_impl.get_buffer(), case[2])
            sessionstate_impl.save_criteria(case[0])

    def test_can_overwrite_selection(self, sessionstate_impl):
        for case in self._random_selections:
            self._write_case_to_buffer(sessionstate_impl.get_buffer(), case[2])
            sessionstate_impl.save_selection(case[0])

    # Tests that overwritten data is not mutated
    def test_overwritten_criteria_persists(self, sessionstate_impl):
        for case in self._random_criteria:
            lines = sessionstate_impl.load_criteria(case[0])

            assert(lines == case[2])

    def test_overwritten_selection_persists(self, sessionstate_impl):
        for case in self._random_selections:
            lines = sessionstate_impl.load_selection(case[0])

            assert(lines == case[2])

    # Tests that data can be deleted
    def test_can_delete_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            sessionstate_impl.delete_criteria(case[0])

    def test_can_delete_selection(self, sessionstate_impl):
        for case in self._random_selections:
            sessionstate_impl.delete_selection(case[0])

    def test_selections_dont_exist_after_deletion(self, sessionstate_impl):
        for case in self._random_selections:
            assert not sessionstate_impl.selection_exists(case[0])

    def test_criteria_dont_exist_after_deletion(self, sessionstate_impl):
        for case in self._random_criteria:
            assert not sessionstate_impl.criteria_exists(case[0])

    # Tests that deleted data cannot be loaded
    def test_cannot_load_deleted_criteria(self, sessionstate_impl):
        for case in self._random_criteria:
            with pytest.raises(FileIOException):
                sessionstate_impl.load_criteria(case[0])

    def test_cannot_load_deleted_selection(self, sessionstate_impl):
        for case in self._random_selections:
            with pytest.raises(FileIOException):
                sessionstate_impl.load_selection(case[0])

    # Tests that things can be saved after being deleted
    def test_can_save_selection_after_deletion(self, sessionstate_impl):
        for case in self._random_selections:
            self._write_case_to_buffer(sessionstate_impl.get_buffer(), case[3])
            sessionstate_impl.save_selection(case[0])

    def test_can_save_criteria_after_deletion(self, sessionstate_impl):
        for case in self._random_criteria:
            self._write_case_to_buffer(sessionstate_impl.get_buffer(), case[3])
            sessionstate_impl.save_criteria(case[0])

    # Tests that saving after deletion saves the correct data
    def test_resaved_selection_persists(self, sessionstate_impl):
        for case in self._random_criteria:
            lines = sessionstate_impl.load_criteria(case[0])

            assert(lines == case[3])

    def test_resaved_criteria_persists(self, sessionstate_impl):
        for case in self._random_selections:
            lines = sessionstate_impl.load_selection(case[0])

            assert(lines == case[3])
