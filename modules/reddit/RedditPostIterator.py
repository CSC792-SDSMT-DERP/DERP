from .RedditPost import RedditPost

from derp.posts import PostIterator

from praw.exceptions import PRAWException as PrawException
from prawcore.exceptions import PrawcoreException


class RedditPostIterator(PostIterator):
    def __init__(self, reddit_module, praw_reddit_or_subreddit, query_string):
        self.__source = praw_reddit_or_subreddit
        self.__query_string = query_string
        self.__derp_module = reddit_module
        self.__current_iterator = None
        self.__last_full_name = None
        self.__count = 0

    def __construct_new_iterator(self):
        # If creating a new child iterator fails, then
        # That's the end of this post iterator
        try:
            # If this isn't the first iterator generated, then continue
            # 'after' the full name of the last yielded post (See Reddit API)
            extra_args = {} if self.__last_full_name is None else {
                "after": self.__last_full_name, "count": self.__count}


            # listing = self.__source.top(params=extra_args)
            listing = self.__source.search(self.__query_string, params=extra_args) if len(
                self.__query_string) else self.__source.hot(params=extra_args)

            self.__current_iterator = iter(listing)
        except (PrawException, PrawcoreException) as e:
            raise StopIteration from e

    def __iter__(self):
        self.__last_full_name = None
        self.__current_iterator = None
        self.__count = 0

        return self

    def __next__(self):
        # Happens on first __next__
        # Raises StopIteration immediately if the source isn't valid
        if self.__current_iterator is None:
            self.__construct_new_iterator()

        result_submission = None
        try:
            # Try to step the iterator, if it hits the end
            # Make a new one
            result_submission = next(self.__current_iterator)
        except StopIteration:
            # Will either succeed, and then yield a new submission, or raise StopIteration
            # again, in which case this post iterator is done
            self.__construct_new_iterator()
            result_submission = next(self.__current_iterator)
        except (PrawException, PrawcoreException) as e:
            raise StopIteration from e

        assert(result_submission is not None)
        self.__last_full_name = result_submission.fullname

        return RedditPost(self.__derp_module, result_submission)
