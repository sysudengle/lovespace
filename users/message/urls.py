from django.conf.urls import patterns, include, url
from message.views import *
from message.ajax import *
from users.views import Lovers
from loveSpace.public import *

urlpatterns = patterns('message.views',
	url(u'^(?P<lid>\d+)/$', user_dispatch(msg)),# this will lead lid to type of unicode
)

urlpatterns += patterns('message.ajax',
	url(u'^sendtext/$', 'send_text'),
	url(u'^getcomment/(?P<mid>\d+)/$', 'get_comment'),
	url(u'^sendcomment/(?P<mid>\d+)/$', 'send_comment'),
	url(u'^image_upload/$', 'uploadify_script'),
	url(u'^deletemessage/$', 'delete_message'),
	url(u'^deletecomment/$', 'delete_comment'),
)
