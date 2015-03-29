import praw
import os
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedditCFB.settings')
from commentfilter.models import Comment, Post, Author, Flair, Parent, Subreddit


USERAGENT = "Pull Karma from r/CFB"
r = praw.Reddit(USERAGENT)

#Get the CFB Subreddit Object
subreddit = r.get_subreddit('cfb+nfl')
comments = praw.helpers.comment_stream(r, subreddit)
# while True:
#     try:
        #Pull Comments with PRAW comment helper set limit to # of comments to pull


        #Loop thru comments and store in the comments that aren't the ID into the defaults dictionary.
i = 0
for comment in comments:
    # Key ID's
    author     = comment.author
    score = 0
    karma = author.get_submitted(limit = None)
    for thing in karma:
        score += thing.score
        try:
            obj_author = Author.objects.get(author=author)
            obj_author.cfb_karma = score

            obj_author.save()
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            i += 1
            print "Not in Model yet!" + str(i)
            pass
    i += 1
    print "The Karma updated!" + str(i)