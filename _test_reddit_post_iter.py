import json
from modules.reddit.RedditPostIterator import RedditPostIterator as RPI
import praw
creds_file = open("reddit_credentials.json", "r")
creds = json.load(creds_file)
reddit = praw.Reddit(**creds, user_agent="python-interface:labs.ipiano.test:v0")
post_iterator = reddit.subreddit("worldnes").search("self:yes", limit=1)
after = None
for post in post_iterator:
    after = post.fullname
    print(post)
    print(after)

print("Get posts in hot after", after)

params = {"after": after}
post_iterator = reddit.subreddit("worldnes").search("self:yes", params=params)

for post in post_iterator:
    print(post)
