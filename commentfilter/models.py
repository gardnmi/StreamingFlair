from django.db import models
# Create your models here.

class Subreddit(models.Model):
    subreddit                           = models.CharField(max_length = 128, default = "None", blank=True, null=True)

    def __unicode__(self):
        return self.subreddit

class Post(models.Model):
    #Post Attributes
    link_id                             = models.CharField(max_length = 128)
    link_title                          = models.TextField()
    link_url                            = models.TextField()
    domain                              = models.TextField()
    num_comments                        = models.IntegerField(default = 0, blank=True, null=True)
    permalink                           = models.TextField()
    url                                 = models.TextField()
    timestamp                           = models.DateTimeField(auto_now_add = True, auto_now = False)
    subreddit                           = models.ForeignKey(Subreddit)

    def __unicode__(self):
        return self.link_id

class Flair(models.Model):
    cleaned_flair                       = models.CharField(max_length = 128, default = "None", blank=True, null=True)
    subreddit                           = models.ForeignKey(Subreddit)

    def __unicode__(self):
        return self.cleaned_flair

class Parent(models.Model):
    parent_comment_id                           = models.CharField(max_length = 128)
    parent_author                               = models.CharField(max_length = 128, default = "None", blank=True, null=True)
    parent_author_flair_css_class               = models.CharField(max_length = 128, default = "None", blank=True, null=True)
    parent_author_flair_text                    = models.CharField(max_length = 128, default = "None", blank=True, null=True)
    parent_body                                 = models.TextField(default = "None")
    parent_body_html                            = models.TextField(default = "None")
    parent_permalink                            = models.TextField()
    timestamp                                   = models.DateTimeField(auto_now_add = True, auto_now = True)
    #p_author                                    = models.ForeignKey(Comment, blank=True, null=True)
    subreddit                                   = models.ForeignKey(Subreddit)

    def __unicode__(self):
        return self.parent_comment_id

class Comment(models.Model):
    # Create Fields for the Comment Object in Reddit API

    #Thing Attributes
    comment_id                          = models.CharField(max_length = 128, unique = True)

    # Comment Attributes
    body                                = models.TextField()
    body_html                           = models.TextField()
    ''' Want to make a created field for a timestamp '''
    comment_permalink                   = models.TextField()

    # Custom
    timestamp                           = models.DateTimeField(auto_now_add = True, auto_now = True)
    updated                             = models.DateTimeField(auto_now_add = False, auto_now = True)
    post                                = models.ForeignKey(Post)
    #author                              = models.ForeignKey(Author)
    parent                              = models.ForeignKey(Parent, blank=True, null=True)
    webdisplay                          = models.BooleanField(default = False)
    subreddit                           = models.ForeignKey(Subreddit)
    author                              = models.CharField(max_length = 128)
    author_flair_css_class              = models.CharField(max_length = 128,  default = "None", blank=False, null=True)
    author_flair_text                   = models.CharField(max_length = 128,  default = "None", blank = False, null= True)
    #comment_karma                       = models.IntegerField(default = 0, blank=True, null=True)
    #link_karma                          = models.IntegerField(default = 0, blank=True, null=True)
    flair                               = models.ForeignKey(Flair)


    def __unicode__(self):
        return self.comment_id

