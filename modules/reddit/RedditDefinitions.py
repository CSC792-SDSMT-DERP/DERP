from derp.exceptions import ModuleInitializationException
from derp.posts import PostDefinition, FieldType


class RedditInitializationException(ModuleInitializationException):
    pass


class RedditPostDefinition(PostDefinition):
    def __init__(self):
        PostDefinition.__init__(self,
                                {
                                    "nsfw": FieldType.BOOLEAN,
                                    "author": FieldType.STRING,
                                    "title": FieldType.STRING,
                                    "upvotes": FieldType.NUMBER,
                                    "date": FieldType.DATE,
                                    "body": FieldType.STRING
                                }
                                )
