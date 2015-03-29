from django.conf.urls import patterns, include, url

#Import so that Static folder can be found.  See the seeting.py file.
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RedditCFB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'commentfilter.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('commentfilter.urls')),


)

#Add so that Static folder can be found.  See the seeting.py file.
# Should be if not settings.DEBUG when live....
#if not settings.DEBUG:
urlpatterns += static(settings.STATIC_URL,
                          document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)





