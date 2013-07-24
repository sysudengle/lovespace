from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from users.models import *
from django.db import connection
from loveSpace import settings
import os.path

def user_dispatch(view):
	def final_render_view(request, *args, **kwargs):
		data = {}
		data['lovers'] = get_lovers_info(kwargs['lid'])
		kwargs = dict(kwargs, **data)
		template_prefix = kwargs['first'] + "_" + kwargs['second']
		if not request.session.get('uid', None):
		# without logging
			template_name = template_prefix + "_am.html"
		elif not request.session.get('lid', None):
		# user without lover
			template_name = template_prefix + "_nlu.html"
		elif request.session['lid'] == long(kwargs['lid']):	# kwargs['lid'] is type of unicode
		# user's lover space
			template_name = template_prefix + "_olu.html"
		else:
		# user to view other's lover space
			template_name = template_prefix + "_ulu.html"
		kwargs['template_name'] = template_name
		return view(request, *args, **kwargs)
	return final_render_view


def get_lovers_info(lid):
	info = {}
	cursor = connection.cursor()
	print lid
	cursor.execute('select * from User,Lovers where (User.id=Lovers.lover1_id or User.id=Lovers.lover2_id) and Lovers.id=' + lid)
	rows = cursor.fetchall()
	print rows
#	print rows
	if rows:
		info['lover1_id'] = rows[0][0]
		info['lover1_name'] = rows[0][1]
		info['lover2_id'] = rows[1][0]
		info['lover2_name'] = rows[1][1]
		info['lid'] = rows[0][7]
		info['lover1_avatar'] = get_avatar(info['lover1_id'], 'avatar')
		info['lover2_avatar'] = get_avatar(info['lover2_id'], 'avatar')
		info['lovers_avatar'] = get_avatar(str(info['lid']), 'loverAvatar')
		info['lovespace'] = rows[0][10]
	return info

def get_avatar(uid, dir_name):
	if os.path.isfile('%s%s/%s.jpg' % (settings.MEDIA_ROOT, dir_name, str(uid))):
		return uid
	else:
		return 'default'
