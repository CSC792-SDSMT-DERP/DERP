"""
MockModule.py

Class definition for the MockModule, used to mock Module behaviors for testing.
"""
from derp.modules.IModule import IModule
from derp.posts.PostDefinition import PostDefinition
from derp.posts.PostDefinition import FieldType
from derp.language.Grammar import Grammar


class MockModule(IModule):

    def name(self):
        return "MockModule"

    def source_grammar(self):
        return Grammar({
            "MOCKMODULE_SOURCE": '"mock"'
        })

    def post_definition(self):
        return PostDefinition({
            "title": FieldType.STRING,
            "points": FieldType.NUMBER,
            "verified": FieldType.BOOLEAN,
            "post": FieldType.DATE,
        })

    def get_posts(self, source_ast, qualifier_tree):
        pass
