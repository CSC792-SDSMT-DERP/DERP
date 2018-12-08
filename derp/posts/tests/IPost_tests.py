import pytest

from derp.modules.IModule import IModule
from derp.posts.PostDefinition import FieldType

@pytest.mark.parallel
@pytest.mark.plugins
class TestIPost:
    def test_definition_is_valid(self, post_impl):
        post_def = post_impl.definition()
        field_defs = post_def.field_definitions()

        for name, t in field_defs.items():
            assert isinstance(name, str)
            assert t in FieldType

    def test_source_is_IModule(self, post_impl):
        assert isinstance(post_impl.source(), IModule)

    def test_definition_matches_sources(self, post_impl):
        post_post_def = post_impl.definition()
        post_field_defs = post_post_def.field_definitions()

        source = post_impl.source()
        module_post_def = source.post_definition()
        module_field_defs = module_post_def.field_definitions()

        assert post_field_defs == module_field_defs

    def test_access_fields(self, post_impl):
        post_def = post_impl.definition()
        field_defs = post_def.field_definitions()

        for name, t in field_defs.items():
            data = post_impl.field_data(name)
            if data is not None:
                assert isinstance(data, t.value)

    def test_about_returns_bool(self, post_impl):
        assert isinstance(post_impl.about("hello world"), bool)

    def test_overrides_str(self, post_impl):
        post_string = str(post_impl)