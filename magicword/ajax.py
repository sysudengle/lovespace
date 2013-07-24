from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.db.models import Q
from magicword.models import *
from users.models import *
from loveSpace import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import time
import os.path

def send_text(request, *args, **kwargs):
	now = time.strftime('%Y-%m-%d %H:%M')
	if request.POST.get('content', None):
		mgw = Magicword(userId = User.objects.get(id = long(request.POST['uid'])),
				loverId = Lovers.objects.get(id = long(request.POST['lid'])),
				time = now,
				content = request.POST['content'])
		mgw.save()
		
		cursor = connection.cursor()
		cursor.execute('select Magicword.id, User.avatar from Magicword, User where User.id=Magicword.userId order by id desc limit 1')
		row = cursor.fetchall()	# row[0][0] represent message id

		data = {'user_name': request.POST['user'],
				'content': request.POST['content'],
				'time': now,
				'lid': request.session['lid'],
				'avatar': row[0][1],
				'user_id': request.session['uid'],
				'mid': row[0][0]}
		return render_to_response('magicword_basic.html', {'single_magicword': data})
	else:
		return HttpResponse('')

def delete_magicword(request, *args, **kwargs):
	result = '0'
	print 'asdqweoooo'
	print request.session['uid']
	print request.POST['uid']
	if request.method == 'POST' and request.session.get('uid', None) and request.session['uid'] == request.POST.get('uid', None):
		print request.POST['mid']
		print 'asdasd'
		Magicword.objects.get(id = long(request.POST['mid'])).delete();
		result = '1'
	return HttpResponse(result)
