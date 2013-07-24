from django.db import models
from users.models import *

class Magicword(models.Model):
	userId = models.ForeignKey(User, db_column = 'userId')
	loverId = models.ForeignKey(Lovers, db_column = 'loverId') # new add
	time = models.DateTimeField()
	content = models.CharField(max_length = 140)

	class Meta:
		db_table = 'Magicword'
#		ordering = ['-time']
