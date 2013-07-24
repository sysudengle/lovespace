from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import auth
from users.views import lover_search, add_concern, delete_concern, list_fans, list_comment
#from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('users.views',
    # Examples:
    url(r'^login/(?P<error>[^/]*)$', 'login'),
    url(r'^login_finish/', 'login_finish'),
    url(r'^register/$', 'register'),
    url(r'^register_finish/$', 'register_finish'),
    url(r'^logout/$', 'logout'),
	url(r'^(?P<id>\d+)/', include('users.urls')),
    # url(r'^loveSpace/', include('loveSpace.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
	url(r'^lovers/search/$', lover_search),
	url(r'^lovers/add_concern/$', add_concern),
	url(r'^lovers/delete_concern/$', delete_concern),
	url(r'^(?P<first>lovers)/(?P<second>fans)/(?P<lid>\d+)/$', list_fans),
	url(r'^(?P<first>lovers)/(?P<second>comment)/(?P<lid>\d+)/$', list_comment),
	url(r'^(?P<first>lovers)/(?P<second>comment)/(?P<lid>\d+)/', list_comment),
	url(r'^(?P<first>lovers)/(?P<second>home)/', include('message.urls')),
	url(r'^(?P<first>lovers)/(?P<second>magic)/', include('magicword.urls')),
    url(r'^lovers/album/', include('album.urls')),
#    url(r'^image/$', upload_file),
)

urlpatterns += patterns((''),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
		#{'document_root': '/home/dengle/web/loveSpace/static/'}
		{'document_root': settings.STATIC_ROOT}
	),
)

