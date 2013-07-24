from django.conf.urls import patterns, include, url
from magicword.views import *
from loveSpace.public import *

urlpatterns = patterns('magicword.views',
	url(u'^(?P<lid>\d+)/$', user_dispatch(magic_word)),# this will lead lid to type of unicode
)

urlpatterns += patterns('magicword.ajax',
	url(u'^sendtext/$', 'send_text'),
	url(u'^deletemagicword/$', 'delete_magicword'),
)
