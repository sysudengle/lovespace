from django.db import connection
from loveSpace.public import *

class MessageManager:
	@staticmethod
	def get_comment_list(lid):
		cursor = connection.cursor()
		cursor.execute('select User.name, User.id, User.avatar, Comment.content, Comment.time, User.sex from User, Message, Comment where User.id=Comment.userId and Message.id=Comment.messageId and Message.loverId=%s order by Comment.id desc' % (lid))
		rows = cursor.fetchall()
		data = []
		for row in rows:
			data.append({'all': row, 'name': row[0], 'uid': row[1], 'avatar': row[2], 'content': row[3], 'time': row[4], 'sex': get_sex(row[5])})
		return {'comments': data}
