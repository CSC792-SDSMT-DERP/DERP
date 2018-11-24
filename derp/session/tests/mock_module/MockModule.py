"""
MockModule.py

Class definition for the MockModule, used to mock Module behaviors for testing.
"""
from derp.modules import IModule
from derp.posts import PostDefinition, FieldType, PostIterator
from derp.language import Grammar

from .MockPost import MockPost

from datetime import date


class MockModule(IModule):

    def __init__(self):
        self.posts = [
            MockPost(self, date(1970, 1, i % 31 + 1), i, chr(i) + "est", i % 2 == 0) for i in range(100)
        ]

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
        return PostIterator(self.filter_posts(qualifier_tree))

    def filter_posts(self, qualifier_tree):
        for post in self.posts:
            if qualifier_tree.evaluate(post):
                yield post
