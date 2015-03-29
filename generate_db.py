import praw
import datetime
import time
import os
import HTMLParser
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedditCFB.settings')
from commentfilter.models import Comment, Post, Flair, Parent, Subreddit
#from commentfilter.views import ajax

def my_long_running_process():
    USERAGENT = "Pull Comments from r/CFB"
    r = praw.Reddit(USERAGENT)
    WAIT = 1
    h = HTMLParser.HTMLParser()


    #Get the CFB Subreddit Object
    subreddit = r.get_subreddit('cfb+nfl+nba+collegebasketball+hockey')
    comments = praw.helpers.comment_stream(r, subreddit)

            #Loop thru comments and store in the comments that aren't the ID into the defaults dictionary.
    i = 0
    for comment in comments:
        # Key ID's
        comment_id = comment.id
        author     = comment.author
        link_id    = comment.link_id
        subreddit  = comment.subreddit

        obj_subreddit, created = Subreddit.objects.get_or_create(subreddit = subreddit)

        # Pack non ID Fields into Defaults for Post Model
        defaults_post    = {
                    'link_title'                          : h.unescape(comment.link_title),
                    'link_url'                            : comment.link_url,
                    #'domain'                              : link_id.domain,
                    #'num_comments'                        : link_id.num_comments,
                    #'permalink'                           : link_id.permalink,
                    #'url'                                 : link_id.url
        }
        obj_post,created = Post.objects.get_or_create(link_id = link_id, defaults = defaults_post, subreddit = obj_subreddit)

        #Allows Filtering of Distinct Flair
        if str(subreddit) == "nhl":
            try:
                cleaned_flair                 = comment.author_flair_css_class
            except AttributeError:
                cleaned_flair                 = 'NoFlair'
            obj_flair, created = Flair.objects.get_or_create(cleaned_flair = cleaned_flair, subreddit = obj_subreddit)
        else:
            try:
                cleaned_flair                    = h.unescape(comment.author_flair_text).split(' / ')[0]
            except TypeError:
                try:
                    cleaned_flair                 = comment.author_flair_text.split(' / ')[0]
                except AttributeError:
                    cleaned_flair                 = 'NoFlair'
            obj_flair, created = Flair.objects.get_or_create(cleaned_flair = cleaned_flair, subreddit = obj_subreddit)

        #Parent Atrributes only if the id contains t1 otherwise they are the Link and we don't want that data.
        parent_id = comment.parent_id
        if 't1' in parent_id:
            parent_comment_id = parent_id
            try:
                parent_comment = Comment.objects.get(comment_id = parent_comment_id[3:])
                defaults_parent    = {
                'parent_author'                               :  parent_comment.author,
#                'parent_author_flair_css_class'               :  parent_comment.author_flair_css_class,
#                'parent_author_flair_text'                    :  parent_comment.author_flair_text,
                'parent_body'                                 :  parent_comment.body,
                'parent_body_html'                            :  parent_comment.body_html
                }
                if not parent_comment.author_flair_css_class:
                    defaults_parent['parent_author_flair_text'] = 'NoFlair'
                    defaults_parent['parent_author_flair_css_class'] = 'NoFlair'
                else:
                    defaults_parent['parent_author_flair_text'] = parent_comment.author_flair_text
                    defaults_parent['parent_author_flair_css_class'] = parent_comment.author_flair_css_class
                if str(subreddit) == 'CFB':
                    defaults_parent['parent_permalink'] = 'http://www.reddit.com/r/cfb/comments/' + link_id[3:] + '//' + parent_comment_id[3:] + '?context=10'
                elif str(subreddit) == 'nba':
                    defaults_parent['parent_permalink'] = 'http://www.reddit.com/r/nba/comments/' + link_id[3:] + '//' + parent_comment_id[3:] + '?context=10'
                elif str(subreddit) == 'CollegeBasketball':
                    defaults_parent['parent_permalink'] = 'http://www.reddit.com/r/collegebasketball/comments/' + link_id[3:] + '//' + parent_comment_id[3:] + '?context=10'
                elif str(subreddit) == 'hockey':
                    defaults_parent['parent_permalink'] = 'http://www.reddit.com/r/hockey/comments/' + link_id[3:] + '//' + parent_comment_id[3:] + '?context=10'
                else:
                    defaults_parent['parent_permalink'] = 'http://www.reddit.com/r/nfl/comments/' + link_id[3:] + '//' + parent_comment_id[3:] + '?context=10'
                obj_parent_comment, created = Parent.objects.get_or_create(parent_comment_id = parent_comment_id, defaults = defaults_parent,  subreddit = obj_subreddit)
            except ObjectDoesNotExist:
                obj_parent_comment = None
        else:
            obj_parent_comment = None

        # Pack non ID Fields into Defaults for Comment Model
        defaults_comments = {
                    # Comment Attributes
                    'body'                                : h.unescape(comment.body),
                    'body_html'                           : h.unescape(comment.body_html),
                    'author'                              :  author,
                    'author_flair_css_class'              :  comment.author_flair_css_class,
                    'author_flair_text'                   :  comment.author_flair_text
                    }
        # This is attribute is slow needs to be manually created
        if not comment.author_flair_css_class:
            defaults_comments['author_flair_text'] = 'NoFlair'
            defaults_comments['author_flair_css_class'] = 'NoFlair'
        else:
            defaults_comments['author_flair_text'] =  comment.author_flair_text
            defaults_comments['author_flair_css_class'] = comment.author_flair_css_class
        if str(subreddit) == 'CFB':
            defaults_comments['comment_permalink'] = 'http://www.reddit.com/r/cfb/comments/' + link_id[3:] + '//' + comment_id + '?context=10'
        elif str(subreddit) == 'nhl':
            defaults_comments['comment_permalink'] = 'http://www.reddit.com/r/nhl/comments/' + link_id[3:] + '//' + comment_id + '?context=10'
        elif str(subreddit) == 'nba':
            defaults_comments['comment_permalink'] = 'http://www.reddit.com/r/nba/comments/' + link_id[3:] + '//' + comment_id + '?context=10'
        elif str(subreddit) == 'CollegeBasketball':
            defaults_comments['comment_permalink'] = 'http://www.reddit.com/r/collegebasketball/comments/' + link_id[3:] + '//' + comment_id + '?context=10'
        elif str(subreddit) == 'hockey':
            defaults_comments['comment_permalink'] = 'http://www.reddit.com/r/hockey/comments/' + link_id[3:] + '//' + comment_id + '?context=10'
        else:
            defaults_comments['comment_permalink'] = 'http://www.reddit.com/r/nfl/comments/' + link_id[3:] + '//' + comment_id + '?context=10'
        #store or get the object into the Model
        try:
            obj, created = Comment.objects.get_or_create(comment_id=comment_id, defaults = defaults_comments, post = obj_post, parent = obj_parent_comment, subreddit = obj_subreddit, flair = obj_flair)
        except:
            pass

        i += 1
        print "Completed " + str(i) + "!"









