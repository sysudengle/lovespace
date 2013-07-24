from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.db.models import Q
from magicword.models import *
from django.db import connection
from loveSpace import settings
from django.views.decorators.csrf import csrf_exempt

def magic_word(request, *args, **kwargs):
	data = []
	cursor = connection.cursor()
	cursor.execute("select Magicword.id, User.name, Magicword.time, Magicword.content, User.id, User.avatar from User, Magicword where User.id=Magicword.userId and Magicword.loverId=" + str(kwargs['lovers']['lid']) + " order by Magicword.id desc")
	rows = cursor.fetchall()
	for row in rows:
		data.append({"all": rows[0], "mid": row[0], "lid": kwargs['lid'], "user_name": row[1], "time": row[2], "content": row[3], "user_id": row[4], 'avatar': row[5]})
	return {"magicword": data}
