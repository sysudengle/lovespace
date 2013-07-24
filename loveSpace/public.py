#-*- coding: UTF-8 -*- 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from users.models import *
from django.db import connection, transaction
from loveSpace import settings
import os.path
import datetime

def user_dispatch(process):
	def final_render_view(request, *args, **kwargs):
		print 'start =========='
		print 'init: ', kwargs
		data = {}
		data['lovers'] = get_lovers_info(kwargs['lid'])
		kwargs = dict(kwargs, **data)
		data = dict(process(request, *args, **kwargs), **data)
		data['fans'] = get_fans(kwargs['lid'])
		template_prefix = kwargs['first'] + "_" + kwargs['second']
		print template_prefix
		print 'data to template: ', data
		if not request.session.get('uid', None):
		# without logging
			print "_am =========="
			return render_to_response(template_prefix + "_am.html", data, context_instance = RequestContext(request))
		elif not request.session.get('lid', None):
		# user without lover
			print "_nlu =========="
			return render_to_response(template_prefix + "_nlu.html", data, context_instance = RequestContext(request))
		elif request.session['lid'] == long(kwargs['lid']):	# kwargs['lid'] is type of unicode
		# user's lover space
			data['inform'] = InfoManager.get_inform(request.session['uid'])
			data['concern'] = get_concern(request.session['uid'])
			data['inform'] = InfoManager.get_inform(request.session['uid'])
			data['concern'] = get_concern(request.session['uid'])
			print "_olu =========="
			return render_to_response(template_prefix + "_olu.html", data, context_instance = RequestContext(request))
		else:
		# user to view other's lover space
			data['inform'] = InfoManager.get_inform(request.session['uid'])
			print "_ulu =========="
			return render_to_response(template_prefix + "_ulu.html", data, context_instance = RequestContext(request))
	return final_render_view


def get_lovers_info(lid):
	info = {}
	cursor = connection.cursor()
	# print lid
	cursor.execute('select * from User,Lovers where (User.id=Lovers.lover1_id or User.id=Lovers.lover2_id) and Lovers.id=' + lid)
	rows = cursor.fetchall()
	print ('select Photo.name from Photo,Album where Album.loversId=' + str(lid) + 'and Album.photonum > 0 and Photo.album_id =Album.id')
	cursor.execute('select Album.loversId,Album.id,Photo.name from Photo,Album where Album.loversId = ' + str(lid) + ' and Album.photonum > 0 and Photo.album_id =Album.id')
	photo = cursor.fetchone()
	print '!!!', photo
	# print rows[0]
	if rows:
		date = rows[0][15]
		# print type(date)
		now = datetime.datetime.now()
		# print type(now)
		date = now.date() - date.date()
		info['lover1_id'] = rows[0][0]
		info['lover1_name'] = rows[0][1]
		info['lover1_sex'] = get_sex(rows[0][4])
		info['lover1_age'] = rows[0][5]
		print "---------------------------------------suck----"
		info['lover1_avatar'] = rows[0][7]
		info['lover2_id'] = rows[1][0]
		info['lover2_name'] = rows[1][1]
		info['lover2_sex'] = get_sex(rows[1][4])
		info['lover2_age'] = rows[1][5]
		info['lover2_avatar'] = rows[1][7]
		info['lid'] = rows[0][8]
		info['lovers_avatar'] = rows[0][14]
		info['time'] = date.days
		info['lovespace'] = rows[0][11]
		if photo:
			info['album_cover'] = str(photo[0]) + '/' + str(photo[1]) + '/' + str(photo[2])
		else:
			info['album_cover'] = 'default_cover.jpg'
	return info

#def get_avatar(uid, dir_name):
#	if os.path.isfile('%s%s/%s.jpg' % (settings.MEDIA_ROOT, dir_name, str(uid))):
#		return uid
#	else:
#		return 'default'
def get_user_info(uid):
	cursor = connection.cursor()
	cursor.execute('select id, name, age, sex, avatar from User where id=%s' % (uid))
	row = cursor.fetchone()
	info = {}
	if row:
		info['uid'] = row[0]
		info['name'] = row[1]
		info['age'] = row[2]
		info['sex'] = get_sex(row[3])
		info['avatar'] = row[4]
	return info

def get_fans(lid):
	cursor = connection.cursor()
	cursor.execute('select User.id, User.name, User.avatar from User,Relation where Relation.to_lid=' + str(lid) + ' and User.id=Relation.from_uid limit 3')
	rows = cursor.fetchall()
	info = []
	for row in rows:
		# print row[0]
		info.append({'all': row[0], 'uid': row[0], 'user_name': row[1], 'avatar': row[2]})
	return info

def get_concern(uid):
	cursor = connection.cursor()
	cursor.execute('select Lovers.id, Lovers.name, Lovers.avatar from Lovers,Relation where Relation.from_uid=' + str(uid) + ' and Lovers.id=Relation.to_lid limit 3')
	rows = cursor.fetchall()
	info = []
	for row in rows:
		# print row[0]
		info.append({'all': row[0], 'lid': row[0], 'lover_name': row[1], 'avatar': row[2]})
	return info

def get_sex(s):
	return (s == 'm') and '男生' or '女生'

class InfoManager:
	@staticmethod
	def init_inform(uid):
		cursor = connection.cursor()
		cursor.execute('insert into FansInform (uid) values (%s)' % (uid))
		cursor.execute('insert into CommentInform (uid) values (%s)' % (uid))

	@staticmethod
	def add_inform(tbl_name, lid):
		tbl = tbl_name + 'Inform'
		cursor = connection.cursor()
		a = 'update %s, Lovers set %s.num=%s.num+1 where (%s.uid=Lovers.lover1_id or %s.uid=Lovers.lover2_id) and Lovers.id=%s' % (tbl, tbl, tbl, tbl, tbl, lid)
		cursor.execute(a)
		transaction.commit_unless_managed()

	@staticmethod
	def get_inform(uid):
		cursor = connection.cursor()
		cursor.execute('select FansInform.num, CommentInform.num from FansInform, CommentInform where FansInform.uid=CommentInform.uid and FansInform.uid=%s' % (uid))
		row = cursor.fetchone()
		row = {'fans': row[0], 'comment': row[1]}
		return row

	@staticmethod
	def delete_inform(tbl_name, uid):
		cursor = connection.cursor()
		cursor.execute('update %sInform set num=0 where uid=%s' % (tbl_name, uid))
		transaction.commit_unless_managed()
