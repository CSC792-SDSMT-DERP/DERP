"""
RedditModule.py

Class definition for the RedditModule, the core module of the language.
"""
from derp.language import Grammar
from derp.posts import PostDefinition, FieldType
from derp.modules import IModule
from derp.exceptions import ModuleInitializationException

import praw
import prawcore


class RedditInitializationException(ModuleInitializationException):
    pass


class RedditModule(IModule):
    def __init__(self, client_id, client_secret, password=None, username=None):
        try:
            user_agent = "dekstop-python:edu.sdsmt.derp.redditmodule:v1 (by {0})".format(
                username)

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
        return PostDefinition(
            {
                "nsfw": FieldType.BOOLEAN,
                "author": FieldType.STRING,
                "title": FieldType.STRING,
                "upvotes": FieldType.NUMBER,
                "date": FieldType.DATE
            }
        )

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
            assert(len(source_ast.children) == 1)

            # Lop off "" surrounding the name
            subreddit_name = source_ast.children[0][1:-1]
            source_reddit = self.__reddit.subreddit(subreddit_name)

        return RedditPostIterator(source_reddit)
