from django.conf.urls import patterns, include, url
from album.views import *

urlpatterns = patterns('',
    # url(u'^(?P<lid>\d+)/page(?P<pid>\d+)/$', album),
	url(u'^(?P<lid>\d+)/page(?P<pid>\d+)/$', user_dispatch(album_show)),
	# (r'^lovers/album/(?P<lid>\d+)/add/$', 'albumAdd'),
    url(u'^(?P<lid>\d+)/(?P<aid>\d+)/page(?P<pid>\d+)/$', user_dispatch(photos_show)),
	url(u'^uploadphoto/$', photos_add),
	url(u'^deletealbum/$', delete_album),
	url(u'^deletephoto/$', delete_photo),
)
