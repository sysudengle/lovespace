from django.conf.urls import patterns, include, url
from users.views import *

urlpatterns = patterns('users.views',
#	url(u'user/$', 'user_deal'),
	url(u'user/$', require_login(user_deal)),
	url(u'user/search/$', require_login(search)),
	url(u'user/add_request/(?P<to_id>\d+)/$', request_lover),
	url(u'user/delete_request/(?P<to_id>\d+)/$', request_delete),
	url(u'user/refuselover/(?P<from_id>\d+)/$', refuse_request),
	url(u'user/acceptlover/(?P<from_id>\d+)/$', accept_request),
)

urlpatterns += patterns('users.views',
	url(u'(?P<lid>\d+)/$', 'lovers_deal'),
)
