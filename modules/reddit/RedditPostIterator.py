from derp.posts import PostIterator

from praw.exceptions import PRAWException as PrawException
from prawcore.exceptions import PrawcoreException


class RedditPostIterator(PostIterator):
    def __init__(self, praw_reddit_or_subreddit):
        self.__source = praw_reddit_or_subreddit

    def __construct_new_iterator(self):
        # If creating a new child iterator fails, then
        # That's the end of this post iterator
        try:
            # If this isn't the first iterator generated, then continue
            # 'after' the full name of the last yielded post (See Reddit API)
            extra_args = {} if self.__last_full_name is None else {
                "after": self.__last_full_name}

            listing = self.__source.top(params=extra_args)
            self.__current_iterator = iter(listing)
        except (PrawException, PrawcoreException) as e:
            raise StopIteration from e

    def __iter__(self):
        self.__last_full_name = None
        self.__current_iterator = None

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

        # TODO : Wrap in a derp.Post type
        return result_submission
