from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext 
from users.models import *
from users.RelationManager import *
from message.MessageManager import *
from django.db.models import Q
from message.models import *
from loveSpace import settings
from django.db import connection
from django.db.models import Q
from loveSpace.public import *
import datetime
import Image
#from django.core.context_processors import csrf

#************************** login system ************************************************
def register(request):
	return render_to_response("register.html", context_instance = RequestContext(request))

def register_finish(request):
	if request.method == 'POST':
		error_list = user_data_valid(request)
		if not error_list:
			write_user_to_db(request)
			request.session['user'] = request.POST['name']
			request.session['uid'] = str(User.objects.get(name = request.POST['name']).id)
			request.session['request_list'] = get_notify_from_request_list(request)
			request.session['lid'] = get_lovers_id(request)
			avatar_process(request, 'avatar', request.session['uid'])
			InfoManager.init_inform(request.session['uid'])
			return HttpResponseRedirect("/" + request.session['uid'] + '/user/')
#			return render_to_response('user_home.html', context_instance = RequestContext(request))
		else:
#			return render_to_response('register.html', {'error_list': error_list}, context_instance = RequestContext(request))
			return HttpResponseRedirect('/register/')
	return HttpResponseRedirect('/register/')

def login(request, error):
	if request.session.get('uid', None):
		return HttpResponseRedirect('/' + request.session['uid'] + "/user/")
	else:
		return render_to_response("login.html", {'error': error}, context_instance = RequestContext(request))

def login_finish(request):
	if request.method == 'POST':
#		if request.session.test_cookie_worked():
#			request.session.delete_cookie()
			#request.session['user'] = request.POST.get('name', '')
		error_list = user_valid(request)
		if not error_list:
			request.session['user'] = request.POST['name']
			request.session['uid'] = str(User.objects.get(name = request.POST['name']).id)
			request.session['request_list'] = get_notify_from_request_list(request)
			request.session['lid'] = get_lovers_id(request)
			print request.session['request_list']
			if request.session['lid']:
				return HttpResponseRedirect("/lovers/home/" + str(request.session['lid']) + "/")
			else:
				return HttpResponseRedirect("/" + request.session['uid'] + '/user/')
		else:
			if error_list[0] == 'name':
				return HttpResponseRedirect('/login/n')	# user does not exist
			else:
				return HttpResponseRedirect('/login/p')	# password input error
#			return render_to_response("login.html", {'error_list': error_list}, context_instance = RequestContext(request))
#		else:
#			return HttpResponse("open cookie")

def logout(request):
	try:
		del request.session['uid']
		del request.session['name']
		del request.session['request_list']
		del request.session['lid']
	except KeyError:
		pass
	# avoid delete session again
	return HttpResponseRedirect('/login/')

#****************************** Use AOP *************************************

# AOP to reduce login test
def require_login(view):
	def new_view(request, *args, **kwargs):
		if not request.session.get('uid', None):
			HttpResponseRedirect('/login/')
		else:
			data = {}
			data['user'] = get_user_info(request.session['uid'])
			print data['user']
			data['concern'] = get_concern(request.session['uid'])
			data['invitions'] = get_notify_from_request_list(request)
			kwargs = dict(kwargs, **data)	
		return view(request, *args, **kwargs)
	return new_view

def user_deal(request, *args, **kwargs):
#	if request.session.get('uid', None):
	try:
		lovers = Lovers.objects.get(Q(lover1_id = int(request.session['uid'])) | Q(lover2_id = int(request.session['uid'])))
	except Lovers.DoesNotExist:
		return render_to_response('user_home.html', kwargs, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/lovers/home/' + str(lovers.id) + "/")

def lovers_deal(request, lid):
	return render_to_response('pair_home.html')

def search(request, *agrs, **kwargs):
	if request.method == 'POST':
		if not request.POST.get('search', None):
			data = RelationManager.get_search_list(request.session['uid'], None, True, request.POST.get('search', None))
			data['concern'] = get_concern(request.session['uid'])
#			userlist = []
#			cursor = connection.cursor()
#			cursor.execute('select User.id, User.name from User where spouseId is null and User.id != ' + id)
#			rows = cursor.fetchall()
#			for row in rows:
#				userlist.append({'all': row, 'id': row[0], 'name': row[1]})
#			userlist = User.objects.filter(spouseId )
		else:
#			userlist = []
			data = []
#	return render_to_response('search.html', {'userlist': userlist}, context_instance = RequestContext(request))
	return render_to_response('search.html', data, context_instance = RequestContext(request))

def request_lover(request, id, to_id):
	request_into_list(request, int(id), int(to_id))
#	return HttpResponseRedirect('/' + request.session['uid'] + '/user/')
	return HttpResponse('y')

def request_delete(request, id, to_id):
	delete_request(request, int(id), int(to_id))
	return HttpResponse('y')

def refuse_request(request, id, from_id):
	delete_request(request, int(id), int(from_id))
	return HttpResponse('y')

def accept_request(request, id, from_id):
	add_request(request, int(from_id), int(id))
	delete_request(request, int(from_id), int(id))
	request.session['lid'] = get_lovers_id(request)
	avatar_process(request, 'loveravatar', str(request.session['lid']))
	os.mkdir('%s%s' % (settings.MEDIA_ROOT, str(request.session['lid'])))
	os.mkdir('%s%s/msg' % (settings.MEDIA_ROOT, str(request.session['lid'])))
	return HttpResponseRedirect('/' + request.session['uid'] + '/user/')

def avatar_process(request, dir_name, id):
	if request.FILES.get('avatar', None):
		cursor = connection.cursor()
		if dir_name == 'loverAvatar':
			table = 'Lovers'
		else:
			table = 'User'
		cursor.execute("update %s set avatar='%s' where id=%s" % (table, id, id))
		avatar_file = '%s%s/%s.jpg' % (settings.MEDIA_ROOT, dir_name, id)
		avatar_file_ss = '%s%s/%s_ss.jpg' % (settings.MEDIA_ROOT, dir_name, id)
		avatar_file_s = '%s%s/%s_s.jpg' % (settings.MEDIA_ROOT, dir_name, id)
		avatar_file_m = '%s%s/%s_m.jpg' % (settings.MEDIA_ROOT, dir_name, id)
		f = open(avatar_file, 'wb+')
		for chunk in request.FILES['avatar'].chunks():	# ensure the big file upload
			f.write(chunk)
		f.close()
		o_img = Image.open(avatar_file)
		width, height = o_img.size
		alpha = float(width) / float(height)
		if alpha > 1:
			m_img = o_img.resize((145, int(145 / alpha)))
			s_img = o_img.resize((75, int(75 / alpha)))
			ss_img = o_img.resize((45, int(45 / alpha)))
		else:
			m_img = o_img.resize((int(alpha * 145), 145))
			s_img = o_img.resize((int(alpha * 75), 75))
			ss_img = o_img.resize((int(alpha * 45), 45))
		m_img.save(avatar_file_m)
		s_img.save(avatar_file_s)
		ss_img.save(avatar_file_ss)
		#ss_img.save(avatar_file_ss)
#		f.write(request.FILES['Filedata'].read())

def lover_search(request, *agrs, **kwargs):
	if request.method == 'POST':
		if request.session.get('lid', None):
			data = RelationManager.get_search_list(request.session['uid'], str(request.session['lid']), False, request.POST.get('search', None))
			data['lovers'] = get_lovers_info(kwargs['lid'])
			print data['lovers']
			print 'fuck'
			data['fans'] = get_fans(kwargs['lid'])
			return render_to_response('lover_search.html', data, context_instance = RequestContext(request))
		elif request.session.get('uid', None):
			return HttpResponseRedirect('/user/search/')
		else:
			data = RelationManager.get_search_list(None, None, False, request.POST.get('search', None))
			return render_to_response('other_search.html', data, context_instance = RequestContext(request))
	return HttpResponse('500')

def add_concern(request, *args, **kwargs):
	if request.POST:
		info = eval(request.POST.keys()[0])
		concern = Relation(from_uid = long(info['uid']), to_lid = long(info['tid']))
		concern.save()
		return HttpResponse('')
	return 'f'

def delete_concern(request, *args, **kwargs):
	if request.POST:
		info = request.POST
		concern = Relation.objects.get(from_uid = long(info['uid']), to_lid = long(info['tid']))
		concern.delete()
		return HttpResponse('')
	return 'f'

@user_dispatch
def list_fans(request, *args, **kwargs):
#	cursor = connection.cursor()
#	cursor.execute('select User.name, User.id from User, Relation where User.id=Relation.from_uid and Relation.to_lid=%s' % (str(kwargs['lid'])))
#	rows = cursor.fetchall()
#	data = []
#	for row in rows:
#		data.append({'all', row, 'name', row[0], 'id', row[1]})
#	return {'fans_list': data }
	return RelationManager.get_fans_list(kwargs['lid'])

@user_dispatch
def list_comment(request, *args, **kwargs):
	InfoManager.delete_inform('Comment', request.session['uid'])
	return MessageManager.get_comment_list(str(request.session['lid']))

@user_dispatch
def list_concern(request, *args, **kwargs):
	return RelationManager.get_concern_list(str(request.session['uid']))

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
