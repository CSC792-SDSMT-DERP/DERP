from .RedditDefinitions import RedditInitializationException, RedditPostDefinition
import prawcore
import praw
from derp.exceptions import ModuleInitializationException

"""
RedditModule.py

Class definition for the RedditModule, the core module of the language.
"""
from derp.language import Grammar
from derp.posts import PostDefinition, FieldType
from derp.modules import IModule
from derp.exceptions import ModuleInitializationException
from derp.qualifiers import *
from modules.reddit.RedditPostIterator import RedditPostIterator

import praw
import prawcore


class RedditModule(IModule):
    def __init__(self, client_id, client_secret, password=None, username=None):
        try:
            user_agent = "dekstop-python:edu.sdsmt.derp.redditmodule:v1 (by /u/CompilersDERP)"

            self.__reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                password=password,
                username=username,
                user_agent=user_agent
            )

            # User is not guaranteed to give username and password, so just assume
            # we're always trying to do read_only
            self.__reddit.read_only = True

            # Retrieve the top post on reddit to verify that credentials are valid
            for top in self.__reddit.front.hot(limit=1):
                pass

        except prawcore.exceptions.OAuthException as e:
            raise RedditInitializationException("Unable to authenticate reddit account: " + str(e)) from e
        except praw.exceptions.ClientException as e:
            raise RedditInitializationException("Unable to connect to reddit: " + str(e)) from e
        except prawcore.exceptions.ResponseException as e:
            raise RedditInitializationException("Unable to access reddit account: " + str(e)) from e

    # Names must be unique when lower case
    def name(self):
        """
        :return: the name of the module
        """
        return "Reddit"

    # Every rule or token must be prefixed with the module name to prevent rule name collisions
    # The only things this grammar may rely on are the following:
    # * The common lark ESCAPED_STRING is part of the grammar
    # * Whitespace will be ignored when parsing
    #
    # One rule must be [module name]_source, this is the rule that's matched
    #   to know when this module is to be used for a query
    # That rule must not begin with _ or ?. It may begin with !. It may be a token (all caps),
    #   or a rule (all lower-case)
    def source_grammar(self):
        """
        :return: the grammar for parsing sources interpreted by this module.
        """
        return Grammar({'reddit_source': ('"reddit"i', '"subreddit"i ESCAPED_STRING')})

    def post_definition(self):
        """
        :return: the PostDefinition which all posts returned from get_posts must match.
        """
        return RedditPostDefinition()

    def get_posts(self, source_ast, qualifier_tree):
        """
        Retrieves posts from a source specified in the source AST which match a
        given qualifier tree.

        :param source_ast: A AST representing the source clause of a selection.
        :param qualifier_tree: A tree representing a logical expression which the posts must match.
        :return: a PostIterator which iterates over the returned set of posts
        """

        source_reddit = self.__reddit.front

        if len(source_ast.children) > 0:
            assert (len(source_ast.children) == 1)

            # Lop off "" surrounding the name
            subreddit_name = source_ast.children[0][1:-1]
            source_reddit = self.__reddit.subreddit(subreddit_name)

        query_string = self._create_query_string(qualifier_tree)

        print(query_string)

        return RedditPostIterator(self, source_reddit, query_string)

    def _create_query_string(self, qualifier_tree):
        query_string = ""
        if isinstance(qualifier_tree, ParentNode):
            joins = {type(AndNode): "AND",
                     type(OrNode): "OR",
                     type(NotNode): "NOT"}
            join_string = joins[type(qualifier_tree)]
            fragments = []

            for child in qualifier_tree.children():
                fragments.append("(" + self._create_query_string(child) + ")")
            fragments = [s for s in fragments if s != ""]
            query_string = join_string.join(fragments)

            if isinstance(qualifier_tree, NotNode):
                query_string = "NOT" + query_string

        elif isinstance(qualifier_tree, FieldCheckNode):
            queries = {"body": "selftext:{0}",
                       "author": "author:{0}",
                       "title": "title:{0}"}
            field = qualifier_tree.field()
            if field == "nsfw":
                query_string = "nsfw:{0}".format("yes" if qualifier_tree.data() else "no")
            else:
                query_string = queries[field].format(qualifier_tree.data())

        return query_string
