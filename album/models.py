from django.db import models
# Create your models here.


class Album(models.Model):
    loversId = models.IntegerField()
    name = models.CharField(max_length = 100)
    descri = models.CharField(max_length = 100)
    time = models.DateTimeField()
    photonum = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['time']
        db_table = 'Album'


class Photo(models.Model):
    album = models.ForeignKey(Album)
    name = models.CharField(max_length = 100, null = True)
    descri = models.CharField(max_length = 100, null = True)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['time']
        db_table = 'Photo'
