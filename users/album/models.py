from django.db import models
# Create your models here.


class Album(models.Model):
    loversId = models.IntegerField()
    name = models.CharField(max_length = 100)
    desc = models.CharField(max_length = 100)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['time']
        db_table = 'Album'


class Photo(models.Model):
    album = models.ForeignKey(Album)
    name = models.CharField(max_length = 100, null = True)
    desc = models.CharField(max_length = 100, null = True)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['time']
        db_table = 'Photo'


class Comment(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.IntegerField(max_length = 11)
    content = models.CharField(max_length = 200, null = True)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['time']
        db_table = 'Pcomment'
