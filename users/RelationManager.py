#-*- coding: UTF-8 -*- 
from django.db import connection
from loveSpace.public import *

class RelationManager:
	@staticmethod
	def get_fans_list(lid):
		cursor = connection.cursor()
		print 'select User.name, User.id, User.avatar from User, Relation where Relation.to_lid=%s' % (lid)
		cursor.execute('select User.name, User.id, User.avatar, User.sex, User.age, User.email from User, Relation where User.id=Relation.from_uid and Relation.to_lid=%s' % (lid))
		rows = cursor.fetchall()
		data = []
		for row in rows:
			data.append({'all': row, 'name': row[0], 'uid': row[1], 'avatar': row[2], 'sex': get_sex(row[3]), 'age': row[4], 'email': row[5]})
		return {'fans_list': data}

	@staticmethod
	def get_concern_list(uid):
		cursor = connection.cursor()
		cursor.execute('select Lovers.name, Lovers.id, Lovers.avatar, Lovers.time from Lovers, Relation where Relation.to_lid=Lovers.id and Relation.from_uid=%s' % (uid))
		rows = cursor.fetchall()
		data = []
		for row in rows:
			data.append({'all': row, 'name': row[0], 'lid': row[1], 'avatar': row[2], 'time': row[3]})
		return {'concern_list': data}

	@staticmethod
	def get_search_list(uid, lid, single, content):
		condition = {}
		to_id = None
		cmd_relation = 'select to_lid from Relation where from_uid=' + uid
		cmd_user = 'select id, name, avatar, sex, age, email from User where true'
		cmd_lover = 'select id, name, avatar, time from Lovers where true'	# added Lover
	
		print content
		if uid:
			cmd_user += ' and id!=' + uid
		if lid:
			cmd_lover += ' and id!=' + lid
		if content:
			cmd_user += " and name like '%%" + content + "%%'"
			cmd_lover += " and name like '%%" + content + "%%'"
		if single:
			cmd_user += ' and spouseId is null'
			cursor = connection.cursor()
			cursor.execute('select to_id from RequestList where from_id=%s' % (uid))
			row = cursor.fetchone()
			if row:
				to_id = row[0]
		cmd_lover_a = cmd_lover + ' and (false'
		cmd_lover_n = cmd_lover + ' and (true'
		cursor = connection.cursor()
		cursor.execute(cmd_relation)
		rows = cursor.fetchall()
		for row in rows:
			cmd_lover_a += ' or id=' + str(row[0])
			cmd_lover_n += ' and id!=' + str(row[0])
		cmd_lover_a += ')'
		cmd_lover_n += ')'
		print cmd_lover_a
		print cmd_lover_n
		userlist = []
		loverlist = []
		if rows:
			cursor.execute(cmd_lover_a)
			rows = cursor.fetchall()
			for row in rows:
				loverlist.append({'all': row, 'lid': row[0], 'name': row[1], 'avatar': row[2], 'time': row[3]})
	
		cursor.execute(cmd_lover_n)
		rows = cursor.fetchall()
		for row in rows:
			loverlist.append({'all': row, 'lid': row[0], 'name': row[1], 'avatar': row[2], 'time': row[3], 'strange': 'y'})
	
		cursor.execute(cmd_user)
		rows = cursor.fetchall()
		for row in rows:
			userlist.append({'all': row, 'uid': row[0], 'name': row[1], 'avatar': row[2], 'sex': get_sex(row[3]), 'age': row[4], 'email': row[5]})
	
		return {'fans_list': userlist, 'concern_list': loverlist, 'to_id': to_id}

def get_sex(s):
	return (s == 'm') and '男生' or '女生'


