from django.shortcuts import render, HttpResponse
# from django.template import Context
from .models import Comment, Post, Flair, Parent, Subreddit
from django.db.models import Count
# from .tables import CommentTable
# from django_tables2   import RequestConfig
# from django.core import serializers
import json
# from django.http import QueryDict
# from django.template import loader
# from django.db.models import Max
# downloaded from djangosnippets.com[942]
from .snippet_942 import render_block_to_string
from django.db.models import Q
import datetime


def home(request):
    template = 'home.html'
#    comments = Comment.objects.extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp').annotate(created_count=Count('id'))
#    topflair = Comment.objects.values('flair__cleaned_flair').exclude(flair__cleaned_flair__contains = 'NoFlair').annotate(flair_count=Count('id')).order_by('-flair_count')[:15]
#    topFlairUser = Comment.objects.values('flair__cleaned_flair').exclude(flair__cleaned_flair__contains = 'NoFlair').annotate(flair_count=Count('author',distinct=True)).order_by('-flair_count')[:15]
#    cfb = Comment.objects.filter(subreddit__id = 2).extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp').annotate(created_count=Count('id'))
#    nfl = Comment.objects.filter(subreddit__id = 5).extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp').annotate(created_count=Count('id'))
#    nba = Comment.objects.filter(subreddit__id = 4).extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp').annotate(created_count=Count('id'))
#    hockey = Comment.objects.filter(subreddit__id = 3).extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp').annotate(created_count=Count('id'))
#    collegebasketball = Comment.objects.filter(subreddit__id = 1).extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp').annotate(created_count=Count('id'))

    return render(request, template, {#'comments' : comments,
                                     # 'cfb'      : cfb,
                                     # 'nfl'      : nfl,
                                     # 'nba'      : nba,
                                     # 'hockey'   : hockey,
                                     # 'collegebasketball'      : collegebasketball,
#                                    #  'topflair': topflair,
#                                    #  'topFlairUser' : topFlairUser,
                                        })

# Create your views here.
def stream(request, subreddit):
    #Set up filter for date range
    template = subreddit + '_stream.html'
    if subreddit == 'test':
        subreddit = 'cfb'

    flair = request.GET.getlist('flair', '')
    flairlist = request.GET.getlist('flair', '')
    post = request.GET.getlist('post', '')
    postlist = request.GET.getlist('post', '')
    #Variables for Queries
    today = datetime.date.today()
    days = datetime.timedelta(days=1)
    begin = today - days
    end = today + days
    #Initial Page Request
    if flair and post:
        comments =  Comment.objects.select_related().filter((reduce(lambda x, y: x | y, [Q(author_flair_text__icontains = flairs) for flairs in flair])),
                post__link_id__in = post, subreddit__subreddit__iexact = subreddit, timestamp__range=(begin, end)).order_by('-timestamp')[:10]
    elif flair:
        comments = Comment.objects.select_related().filter(reduce(lambda x, y: x | y, [Q(author_flair_text__icontains = flairs) for flairs in flair]),
                    subreddit__subreddit__iexact = subreddit, timestamp__range=(begin, end)).order_by('-timestamp')[:10]
    elif post:
        comments =  Comment.objects.select_related().filter(~Q(flair__cleaned_flair = flair, timestamp__range=(begin, end)), post__link_id__in = post,  subreddit__subreddit__iexact = subreddit).order_by('-timestamp')[:20]
    else:
        comments = Comment.objects.select_related().filter(subreddit__subreddit__iexact = subreddit, timestamp__range=(begin, end)).order_by('-timestamp')[:10]
    posts    = Post.objects.values('link_title', 'link_id').filter(timestamp__range=(begin, end), subreddit__subreddit__iexact = subreddit).order_by('link_title')
    flairs   = Flair.objects.values('cleaned_flair').filter(subreddit__subreddit__iexact = subreddit).order_by('cleaned_flair')
    return render(request, template, {'comments'  : comments ,
                                      'flairs'    :  flairs,
                                      'posts'     : posts,
                                      'flairlist' : flairlist,
                                      'postlist'  : postlist,
                                     }
                  )

def ajaxupdate(request ,subreddit):
    # Ajax GET request
    template = subreddit + '_stream.html'
    if subreddit == 'test':
        subreddit = 'cfb'

    if request.is_ajax():
        since = json.loads(request.GET.get('currentsince','' ))
        flair = json.loads(request.GET.get('flair','' ))
        post = json.loads(request.GET.get('post','' ))
        since = datetime.datetime.fromtimestamp(int(since))
        print since
        flair = flair.encode('UTF8')
        flair = flair.split("'")
        flair = [item for index, item in enumerate(flair) if index % 2 != 0]
        post = post.encode('UTF8')
        post = post.split("'")
        post = [item for index, item in enumerate(post) if index % 2 != 0]

        if flair and post:
            print "Both were ran"
            #Filters Both Flair and Link
            comments =  Comment.objects.select_related().filter((reduce(lambda x, y: x | y, [Q(author_flair_text__icontains = flairs) for flairs in flair])),
                post__link_id__in = post,timestamp__gt=since,  subreddit__subreddit__iexact = subreddit).order_by('-timestamp')
            return_str = render_block_to_string(template, 'ajaxupdate', {'comments': comments})
            return HttpResponse(return_str)
        elif flair:
            print "Flair was ran"
            #Filters only Flair
            comments =  Comment.objects.select_related().filter((reduce(lambda x, y: x | y, [Q(author_flair_text__icontains = flairs) for flairs in flair])),timestamp__gt=since,  subreddit__subreddit__iexact = subreddit).order_by('-timestamp')
            return_str = render_block_to_string(template, 'ajaxupdate', {'comments': comments})
            return HttpResponse(return_str)
        elif post:
            print "Post was ran"
            #Filters only Post
            comments =  Comment.objects.select_related().filter(~Q(flair__cleaned_flair = flair), post__link_id__in = post,timestamp__gt=since, subreddit__subreddit__iexact = subreddit).order_by('-timestamp')
            return_str = render_block_to_string(template, 'ajaxupdate', {'comments': comments})
            return HttpResponse(return_str)
        else:
            print "All was ran"
            #Returns All Comments
            comments =  Comment.objects.select_related().filter(timestamp__gt=since,  subreddit__subreddit__iexact = subreddit).order_by('-timestamp')
            return_str = render_block_to_string(template, 'ajaxupdate', {'comments': comments})
            return HttpResponse(return_str)

def google9b7d68b79cb40779(request ,template = 'google9b7d68b79cb40779.html'):
    return render(request, template, {})

def analysis(request):
    today = datetime.date.today()
    days = datetime.timedelta(days=1)
    begin = today - days
    end = today + days
    print "running analysis"
    subreddit = request.GET.getlist('subreddit', '')
    print subreddit
    template = 'analysis.html'
    comments = Comment.objects.extra({'timestamp':"date(CONVERT_TZ(timestamp,'GMT','EST'))"}).values('timestamp','subreddit__subreddit').filter((reduce(lambda x, y: x | y, [Q(subreddit__subreddit__icontains = subreddits) for subreddits in subreddit])),timestamp__range=(begin, end)).annotate(created_count=Count('id'))
    topflair = Comment.objects.values('flair__cleaned_flair').exclude(flair__cleaned_flair__contains = 'NoFlair').filter((reduce(lambda x, y: x | y, [Q(subreddit__subreddit__icontains = subreddits) for subreddits in subreddit]))).annotate(flair_count=Count('id')).order_by('-flair_count')[:10]
    topflairall = Comment.objects.values('flair__cleaned_flair').exclude(flair__cleaned_flair__contains = 'NoFlair').filter((reduce(lambda x, y: x | y, [Q(subreddit__subreddit__icontains = subreddits) for subreddits in subreddit]))).annotate(flair_count=Count('author',distinct=True)).order_by('-flair_count')[:50]
    topFlairUser = topflairall[:10]
    topUser = Comment.objects.values('author').filter((reduce(lambda x, y: x | y, [Q(subreddit__subreddit__icontains = subreddits) for subreddits in subreddit]))).annotate(flair_count=Count('id')).order_by('-flair_count')[:10]

    return render(request, template, {'comments' : comments,
                                      'topUser'   : topUser,
                                      'topflair': topflair,
                                      'topFlairUser' : topFlairUser,
                                      'topflairall' : topflairall,
                                        })

# def ajax(request ,template = 'cfb_stream.html'):
#     #Set up filter for date range
#     today = datetime.date.today()
#     days = datetime.timedelta(days=2)
#     begin = today - days
#     end = today + days
#     x = 0
#     y = 5
#     # Ajax GET request
#     if request.is_ajax():
#         #Global in order to use variable in ajaxupdate() function
#         flair = json.loads(request.GET.get('flair','' ))
#         post = json.loads(request.GET.get('post','' ))
#         print type(flair)
#         print post
#         if flair and post:
#             #Filters Both Flair and Link
#             comments =  Comment.objects.select_related().filter((reduce(lambda x, y: x | y, [Q(author_flair_text__icontains = flairs) for flairs in flair])),
#                 post__link_id__in = post, subreddit__subreddit= 'CFB').order_by('-timestamp')[:2000]
#             return_str = render_block_to_string(template, 'ajax', {'comments': comments})
#             return HttpResponse(return_str)
#         elif flair:
#             #Filters only Flair
#             comments =  Comment.objects.select_related().filter((reduce(lambda x, y: x | y, [Q(author_flair_text__icontains = flairs) for flairs in flair])), subreddit__subreddit= 'CFB').order_by('-timestamp')[:20]
#             return_str = render_block_to_string(template, 'ajax', {'comments': comments})
#             return HttpResponse(return_str)
#         elif post:
#             #Filters only Post
#             comments =  Comment.objects.select_related().filter(~Q(flair__cleaned_flair = flair), post__link_id__in = post,  subreddit__subreddit= 'CFB').order_by('-timestamp')[:20]
#             return_str = render_block_to_string(template, 'ajax', {'comments': comments})
#             return HttpResponse(return_str)
#         else:
#             #Returns All Comments
#             comments =  Comment.objects.select_related().filter(subreddit__subreddit= 'CFB').order_by('-timestamp')[:10]
#             return_str = render_block_to_string(template, 'ajax', {'comments': comments})
#             return HttpResponse(return_str)


