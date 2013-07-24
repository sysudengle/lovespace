from django.db import models
import hashlib
from django.db import connection
from django.db.models import Q
# Create your models here.

class User(models.Model):
	name = models.CharField(max_length = 15, unique = True)
	password = models.CharField(max_length = 50)
	email = models.EmailField(unique = True)
	sex = models.CharField(max_length = 1)
	age = models.IntegerField(max_length = 11)
	spouseId = models.IntegerField(max_length = 11, null = True)

	class Meta:
		db_table = 'User'

class Lovers(models.Model):
	lover1_id = models.IntegerField(max_length = 11, unique = True)
	lover2_id = models.IntegerField(max_length = 11, unique = True)
	fans = models.IntegerField(max_length = 11)
	notice = models.IntegerField(max_length = 11)
	time = models.DateTimeField()
	name = models.CharField(max_length = 20)

	class Meta:
		db_table = 'Lovers'

class Relation(models.Model):
	from_uid = models.IntegerField(max_length = 11)
	to_lid = models.IntegerField(max_length = 11)
	class Meta:
		db_table = 'Relation'

class RequestList(models.Model):
	from_id = models.IntegerField(max_length = 11, unique = True)
	to_id = models.IntegerField(max_length = 11)
	class Meta:
		db_table = 'RequestList'
'''
@ user operate functions
'''

def user_data_valid(request):
	error_list = []
	if not request.POST.get('name', ''):
		error_list.append("no name")
	if not request.POST.get('password', ''):
		error_list.append("no password")
	if not request.POST.get('email', ''):
		error_list.append("no email")
	if not request.POST.get('sex', ''):
		error_list.append("no age")
	return error_list

def write_user_to_db(request):
	passwd = hashlib.sha1(request.POST['password']).hexdigest()	# use sha1 to encrypt
	user_model = User(name = request.POST['name'],
			password = passwd,
			email = request.POST['email'],
			sex = request.POST['sex'],
			age = int(request.POST['age']),)
	user_model.save()

def user_valid(request):
	error_list = []
	try:
		user = User.objects.get(name = request.POST['name'])
		passwd = hashlib.sha1(request.POST['password']).hexdigest()
		print user.password
		if passwd != user.password:
			error_list.append("pwd")
	except User.DoesNotExist:
		error_list.append("name")
	return error_list

def get_notify_from_request_list(request):
	'''try:
		all_request_users = RequestList.objects.get(to_id = request.session['uid'])
	except RequestList.DoesNotExist:
		pass
	else:
		for from_user in all_request_users:
			request_list.append((int(from_user.from_id), from_use)
	'''
	request_list = []
	cursor = connection.cursor()
	cursor.execute('select User.id, User.name, User.avatar from User, RequestList where User.id=RequestList.from_id and RequestList.to_id=' + request.session['uid'])
	rows = cursor.fetchall()
	print rows
	for row in rows:
		request_list.append({'uid': row[0], 'name': row[1], 'avatar': row[2]})
	print request_list
	return request_list

def request_into_list(request, f_id, t_id):
	try:
		request_info = RequestList(from_id = f_id, to_id = t_id)
	except "error":
		pass
	else:
		request_info.save()

def delete_request(request, f_id, t_id):
	request_info = RequestList.objects.get(from_id = f_id, to_id = t_id)
	request_info.delete()

def add_request(request, f_id, t_id):
	request_info = Lovers(lover1_id = f_id, lover2_id = t_id, name=request.POST.get('lover_name', ''), time = request.POST['date'])
	cursor = connection.cursor()
	cursor.execute('update User set spouseId=%d where id=%d' % (f_id, t_id))
	cursor.execute('update User set spouseId=%d where id=%d' % (t_id, f_id))
	request_info.save()

def get_lovers_id(request):
	try:
		lovers = Lovers.objects.get(Q(lover1_id = request.session['uid']) | Q(lover2_id = request.session['uid']))
	except Lovers.DoesNotExist:
		return None
	else:
		if lovers:
			return lovers.id
		else:
			return None 
