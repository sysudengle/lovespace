from django.db import models
from users.models import *

# Create your models here.
class Message(models.Model):
	userId = models.ForeignKey(User, db_column = 'userId')
	loverId = models.ForeignKey(Lovers, db_column = 'loverId') # new add
	time = models.DateTimeField()
	content = models.CharField(max_length = 140)
	image = models.CharField(max_length = 1)

	class Meta:
		db_table = 'Message'
		ordering = ['-time']

class Comment(models.Model):
	userId = models.IntegerField(max_length = 11)
	time = models.DateTimeField()
	content = models.CharField(max_length = 100)
	messageId = models.ForeignKey(Message, db_column = 'messageId')
	class Meta:
		db_table = 'Comment'
