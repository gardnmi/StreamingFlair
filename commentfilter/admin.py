from django.contrib import admin

# Register your models here.
from .models import Comment, Post, Flair, Parent, Subreddit

class CommentAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','timestamp','updated','body','author_flair_text','subreddit']
    class Meta:
        model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','link_title','id']
    class Meta:
        model = Post


class FlairAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','id']
    class Meta:
        model = Flair

class ParentAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'parent_body']
    class Meta:
        model = Parent

class SubredditAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'subreddit','id']
    class Meta:
        model = Subreddit



admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Flair, FlairAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Subreddit, SubredditAdmin)

