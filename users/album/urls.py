from django.conf.urls import patterns, include, url
from album.views import *

urlpatterns = patterns('',
    url(u'^(?P<lid>\d+)/page(?P<pid>\d+)/$', album),
    # (r'^lovers/album/(?P<lid>\d+)/add/$', 'albumAdd'),
    url(u'^(?P<lid>\d+)/(?P<aid>\d+)/page(?P<pid>\d+)/$', albumPhoto),
)
