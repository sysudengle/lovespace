from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.db.models import Q
from message.models import *
from users.models import *
from loveSpace import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from loveSpace.public import *
import time
import os.path
import Image

def send_text(request, *args, **kwargs):
#	return HttpResponse("shit!")
	now = time.strftime('%Y-%m-%d %H:%M')
#	now = '2013-5-27 2:27'
	print request.POST
	info = eval(request.POST.keys()[0])
#	print dl['name']
	print '1'
	print info
	print info.get('content', None)
	if info.get('content', None):
		img_exist = os.path.isfile('%s%s/temp%s.jpg' % (settings.MEDIA_ROOT, request.session['lid'], request.session['uid']))
		print img_exist
		print info['content']
		if img_exist:
			img_exist = '1'
		else:
			img_exist = '0'
		print img_exist
		msg = Message(userId = User.objects.get(id = long(info['uid'])),
				loverId = Lovers.objects.get(id = long(info['lid'])),
				time = now,
				content = info['content'], image = img_exist)
#		msg = Message(userId = info['uid'], loverId = info['lid'], time = now, content = info['content'])
#		msg = Message(userId = 1, loverId = 6, time = now, content = info['content'])
#		msg = Message(userId_id = long(info['uid']),
		#		loverId_id = long(info['lid']),
		#		time = now,
		#		content = info['content'],
		#)
		msg.save()
		cursor = connection.cursor()
		cursor.execute('select id, image from Message order by id desc limit 1')
		row = cursor.fetchall()	# row[0][0] represent message id
		
		if long(img_exist):
			move_image_to_dir(request, row[0][0])

		if os.path.isfile('%savatar/%s.jpg' % (settings.MEDIA_ROOT, info['uid'])):
			avatar = '%s_s.jpg' % (info['uid'])
		else:
			avatar = 'default_s.jpg'
		data = {'user_name': info['user'],
				'mid': row[0][0], 'content': info['content'],
				'time': now, 'image': long(img_exist),
				'lid': request.session['lid'], 'avatar': avatar,
				'uid': info['uid']}
		return render_to_response('message_basic.html', {'single_message': data})
#		return render_to_response('single_message.html',
#				{'content': request.POST['content'],
#			'uid': request.POST['uid'],
#			'user': request.POST['user'],
#			'time': now})
	else:
		print 'suck'
		return HttpResponse('2')

def get_comment(request, *args, **kwargs):
	if request.method == 'POST':
		data = []
		cursor = connection.cursor()
		cursor.execute('select User.name, User.id, Comment.content, Comment.time, Comment.messageId, Comment.id from User, Comment where User.id=Comment.userId and Comment.messageId=' + request.POST['mid'] + " order by Comment.id desc")
		rows = cursor.fetchall()
		for row in rows:
			data.append({"all": rows[0], "user_name": row[0], "user_id": row[1], "content": row[2], "time": row[3], "mid": row[4], "cid": row[5]})
		return render_to_response('get_comment.html', {"comments": data}, context_instance = RequestContext(request))
	else:
		return HttpResponse('')

def send_comment(request, *args, **kwargs):
	if request.method == 'POST' and request.POST.get('uid', None) and request.POST.get('content', None):
		uid = long(request.POST['uid'])
		now = time.strftime('%Y-%m-%d %H:%M')
		p = Comment(userId = uid, time = now, content = request.POST['content'], messageId = Message.objects.get(id = long(request.POST['mid'])))
		p.save()
		cursor = connection.cursor()
		cursor.execute('select id from Comment order by id desc limit 1')
		row = cursor.fetchall()	# row[0][0] represent message id
		data = {'user_name': User.objects.get(id = uid).name,
				'user_id': uid,
				'content': request.POST['content'],
				'time': now,
				'mid': request.POST['mid'],
				'cid': row[0][0]}
		InfoManager.add_inform('Comment', request.POST['lid'])
		return render_to_response('comment_basic.html', {'comment': data}, context_instance = RequestContext(request))
	else:
		return HttpResponse('')

def move_image_to_dir(request, mid):	#judge whether message should contain image
	basic_path = '%s%s/' % (settings.MEDIA_ROOT, request.session['lid'])
	temp_file = '%stemp%s.jpg' % (basic_path, request.session['uid'])
	temp_s_file = '%stemp_s%s.jpg' % (basic_path, request.session['uid'])
	dest_file = '%smsg/%s.jpg' % (basic_path, mid)
	dest_file_m = '%smsg/%sm.jpg' % (basic_path, mid)	#resize to smallest
	os.remove(temp_s_file)	#delete small temp image
	os.rename(temp_file, dest_file)

	o_img = Image.open(dest_file)
	width, height = o_img.size
	alpha = float(width) / float(height)
	m_img = o_img.resize((int(alpha * 100), 100))

	m_img.save(dest_file_m)

def handle_uploaded_file(f):
	print f.name
	print "cao"
	dest = open('%s%s' % (settings.MEDIA_ROOT, 'dl.jpg'), 'wb+')
	for chunk in f.chunks():
		dest.write(chunk)
	dest.close()

'''@csrf_exempt
def uploadify_script1(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		print request.FILES['file'].chunks()
		print form.is_valid()
		if 1:
			print "jin"
			handle_uploaded_file(request.FILES['file'])
	return HttpResponse('nu cao!')'''

@csrf_exempt
def uploadify_script(request, *args, **kwargs):
	result = '0'
	if request.method == 'POST' and request.FILES['Filedata'] and request.POST.get('lid', None):
		o_tempfile = '%s%s%s' % (settings.MEDIA_ROOT, request.POST['lid'], '/temp' + request.session['uid'] + '.jpg')
		print request.session['uid']
		print request.POST['lid']
		s_tempfile = '%s%s%s' % (settings.MEDIA_ROOT, request.POST['lid'], '/temp_s' + request.session['uid'] + '.jpg')
		print o_tempfile
		f = open(o_tempfile, 'wb+')
		for chunk in request.FILES['Filedata'].chunks():	# ensure the big file upload
			f.write(chunk)
#		f.write(request.FILES['Filedata'].read())
		f.close()
		o_img = Image.open(o_tempfile)
		width, height = o_img.size
		alpha = float(width) / float(height)
		s_img = o_img.resize((int(alpha * 60), 60))
		print s_img
		print 'come on!'
		print s_tempfile
		s_img.save(s_tempfile)
		result = '1'
	return HttpResponse(result)

def delete_message(request, *args, **kwargs):
	result = '0'
	if request.method == 'POST' and request.session.get('uid', None) == request.POST['uid']:
		mid = request.POST['mid']
		Message.objects.get(id = long(mid)).delete()
		basic_path = '%s%s/' % (settings.MEDIA_ROOT, request.POST['lid'])
		dest_file = '%smsg/%s.jpg' % (basic_path, mid)
		if os.path.isfile(dest_file):
			os.remove('%smsg/%s.jpg' % (basic_path, mid))
			os.remove('%smsg/%sm.jpg' % (basic_path, mid))
		result = '1'
	return HttpResponse(result)

def delete_comment(request, *args, **kwargs):
	result = '0'
	if request.method == 'POST' and request.session.get('uid', None) and request.session['uid'] == request.POST.get('uid', None):
		Comment.objects.get(id = long(request.POST['cid'])).delete();
		result = '1'
	return HttpResponse(result)
