from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext 
from django.db.models import Q
from message.models import *
from django.db import connection
from loveSpace import settings
from django.views.decorators.csrf import csrf_exempt
#from django.core.context_processors import csrf

class UploadFileForm(forms.Form):
#	title = forms.CharField(max_length = 50)
	file = forms.FileField()

def msg(request, *args, **kwargs):
	data = []
	cursor = connection.cursor()
	cursor.execute("select Message.id, User.name, Message.time, Message.content, Message.image, User.id from User, Message where User.id=Message.userId and Message.loverId=" + str(kwargs['lovers']['lid']) + " order by Message.id desc")
	rows = cursor.fetchall()
	for row in rows:
		img_exist = row[4]
		img_exist = long(img_exist)
		data.append({"all": rows[0], "mid": row[0], "lid": kwargs['lid'], "user_name": row[1], "time": row[2], "content": row[3], "image": img_exist, 'user_id': row[5]})
	data = dict(kwargs, **data)
	return render_to_response(kwargs['template_name'], data, context_instance = RequestContext(request))

# just test here!
def upload_file(request):
	print "gan"
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		print request.FILES['file'].chunks()
		print form.is_valid()
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
	else:
		form = UploadFileForm()
	return HttpResponse('shit!')

def handle_uploaded_file(f):
	print f.name
	print "cao"
	dest = open('%s%s' % (settings.MEDIA_ROOT, 'dl.jpg'), 'wb+')
	for chunk in f.chunks():
		dest.write(chunk)
	dest.close()

# test end
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
