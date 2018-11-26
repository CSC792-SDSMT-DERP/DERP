from derp.posts import IPost

from .RedditDefinitions import RedditPostDefinition

from praw import Reddit
from praw.models import Redditor

from datetime import datetime


class RedditPost(IPost):
    def __init__(self, parent, praw_submission):
        self.__submission = praw_submission
        self.__parent = parent

        # Mapping from reddit module field names to functions to get the data
        # out of the post
        self.__get_field = {
            "nsfw": self.__get_nsfw,
            "author": self.__get_author,
            "title": self.__get_title,
            "upvotes": self.__get_upvotes,
            "date": self.__get_date,
            "body": self.__get_body
        }

        # Verify that we have a handler function for every field defined for the
        # module
        assert(set(self.__get_field.keys()) == set(
            RedditPostDefinition().field_definitions().keys()))

        # This forces the entire submission to load, making it non-lazy
        # So we can use getattr to check if things exist or not
        # There's no hard rules for what attributes will actually be included
        # in the submission, so all of the checks below are going to essentially be
        # 'check all known attributes, return the first one that's not None, else return None'
        t = self.__submission.title
        self.__sub_data = vars(self.__submission)

    def __get_nsfw(self, submission):
        if "nsfw" in self.__sub_data:
            return self.__sub_data["nsfw"]

        if "over_18" in self.__sub_data:
            return self.__sub_data["over_18"]

        return None

    def __get_body(self, submission):
        if "selftext" in self.__sub_data:
            return self.__sub_data["selftext"]

        return None

    def __get_author(self, submission):
        if "author" in self.__sub_data:
            return self.__sub_data["author"].name

        return None

    def __get_title(self, submission):
        if "title" in self.__sub_data:
            return self.__sub_data["title"]

        return None

    def __get_upvotes(self, submission):
        if "score" in self.__sub_data:
            return self.__sub_data["score"]

        if "ups" in self.__sub_data and "downs" in self.__sub_data:
            return self.__sub_data["ups"] - self.__sub_data["downs"]

        return None

    def __get_date(self, submission):
        try:
            if "created_utc" in self.__sub_data:
                date_utc = self.__sub_data["created_utc"]

                dt = datetime.fromtimestamp(date_utc).date()
                return dt
        except OverflowError as e:
            return None

    def _submission(self):
        return self.__submission

    def definition(self):
        """
        Retrieves the PostDefinition for a given post
        :return: a PostDefinition object describing the fields contained in this post.
        """
        return RedditPostDefinition()

    def source(self):
        """
        Returns the module object which created a given post
        :return: the module object which created this post
        """
        return self.__parent

    def field_data(self, field_name):
        """
        Retrieves the data for a given field.
        It is highly suggested that implementors memoize this function.
        :param field_name: The name of the field to retrieve data for.
        :return: Field data matching the FieldType declared in the PostDefinition
        """
        field = field_name.lower()
        return self.__get_field[field](
            self.__submission) if field in self.__get_field else None

    def about(self, string):
        """
        Decides whether the field data contained in the post matches a given search string.
        :param string: the search string to consider
        :return: True if the post matches, and False if it does not.
        """
        return string in self.__submission.title or string in self.__submission.selftext
