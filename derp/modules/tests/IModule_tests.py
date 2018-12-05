import pytest

from derp.language import *
from derp.posts import PostDefinition, FieldType, IPost

from lark import Transformer


class TestIModule:
    def module_is_valid(self, module_impl):
        try:
            self.test_can_build_grammars(module_impl)
            self.test_name_is_str(module_impl)
            self.test_post_definition(module_impl)
            self.test_post_field_types(module_impl)
            self.test_post_field_types(module_impl)
            self.test_source_grammar_has_modulename_source(module_impl)
            self.test_source_grammar_has_no_start_sym(module_impl)
            self.test_source_grammar_rules_begin_with_module_name(module_impl)

        except Exception:
            return False
        return True

    def test_name_is_str(self, module_impl):
        assert isinstance(module_impl.name(), str)

    def test_source_grammar_rules_begin_with_module_name(self, module_impl):
        module_name = module_impl.name().lower()
        grammar = module_impl.source_grammar()

        for rule, productions in grammar.productions():
            while rule[0] in '?!_':
                rule = rule[1:]

            assert len(rule)
            assert rule.lower().startswith(module_name)

    def test_source_grammar_has_no_start_sym(self, module_impl):
        assert module_impl.source_grammar().start_symbol() is None

    def test_source_grammar_has_modulename_source(self, module_impl):
        module_name = module_impl.name().lower()
        grammar = module_impl.source_grammar()
        target_rule = module_name + "_source"

        source_productions = None
        for rule, productions in grammar.productions():
            while rule[0] in '?!_':
                rule = rule[1:]
            if rule.lower() == target_rule:
                source_productions = productions
                break

        assert source_productions is not None

        for prod in source_productions:
            assert "->" not in prod

    def test_can_build_grammars(self, module_impl):
        build_selection_and_criteria_parsers([module_impl])

    def test_post_definition(self, module_impl):
        pd = module_impl.post_definition()

        assert isinstance(pd, PostDefinition)

    def test_post_field_types(self, module_impl):
        pd = module_impl.post_definition()
        fd = pd.field_definitions()

        for k, t in fd.items():
            assert t in FieldType

    class __AddParseTreeCleanup(Transformer):
        def statement(self, children):
            return children[0]

        def add_expression(self, children):
            return children[0]

        def selector(self, children):
            return children[0]

        def source_module(self, children):
            return children[0]

    def test_get_posts_no_qualifiers(self, module_impl, module_source_string):
        parser1, parser2 = build_selection_and_criteria_parsers([module_impl])
        tree = parser1.parse("add posts from" + module_source_string)

        tree = self.__AddParseTreeCleanup().transform(tree)
        iterator = module_impl.get_posts(tree, None)

        # Try to get a post out of it; but maybe there just aren't any
        try:
            assert isinstance(next(iterator), IPost)
        except StopIteration:
            pass
