from django.conf.urls import patterns, url
from commentfilter import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^analysis', views.analysis, name='analysis'),
        url(r'^(?P<subreddit>\w+)$', views.stream, name='stream'),
        url(r'^(?P<subreddit>\w+)/ajaxupdate/$', views.ajaxupdate, name='ajaxupdate'),
        url(r'^google9b7d68b79cb40779.html$', views.google9b7d68b79cb40779, name='google9b7d68b79cb40779'),



#        url(r'^nfl$', views.nfl_stream, name='nfl_stream'),
#        url(r'^nhl$', views.nhl_stream, name='nhl_stream'),
#        url(r'^nba$', views.nba_stream, name='nba_stream'),
#        url(r'^collegebasketball$', views.collegebasketball_stream, name='collegebasketball_stream'),
#        url(r'^collegehockey$', views.collegehockey_stream, name='collegehockey_stream'),
#        url(r'^cfb_ajax/', views.cfb_ajax, name='cfb_ajax'),
#        url(r'^nfl_ajax/', views.nfl_ajax, name='nfl_ajax'),
#        url(r'^nhl_ajax/', views.nhl_ajax, name='nhl_ajax'),
#        url(r'^nba_ajax/', views.nba_ajax, name='nba_ajax'),
#        url(r'^collegebasketball_ajax/', views.collegebasketball_ajax, name='collegebasketball_ajax'),
#        url(r'^collegehockey_ajax/', views.collegehockey_ajax, name='collegehockey_ajax'),
#        url(r'^cfb_ajaxupdate/', views.cfb_ajaxupdate, name='cfb_ajaxupdate'),
#        url(r'^nfl_ajaxupdate/', views.nfl_ajaxupdate, name='nfl_ajaxupdate'),
#        url(r'^nba_ajaxupdate/', views.nba_ajaxupdate, name='nba_ajaxupdate'),
#        url(r'^nhl_ajaxupdate/', views.nhl_ajaxupdate, name='nhl_ajaxupdate'),
#        url(r'^collegebasketball_ajaxupdate/', views.collegebasketball_ajaxupdate, name='collegebasketball_ajaxupdate'),
#        url(r'^collegehockey_ajaxupdate/', views.collegehockey_ajaxupdate, name='collegehockey_ajaxupdate'),


       )



