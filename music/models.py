from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from image_cropping import ImageRatioField
from datetime import datetime

class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=250)
    album_logo = models.ImageField(null=True, blank= True, height_field="height_field",width_field="width_field")
    height_field=models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    genre = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default = None)
    created = models.DateTimeField(auto_now_add=True, blank=True)


    def get_absolute_url(self):
        return reverse( 'music:detail', kwargs={'pk': self.pk})

    def __str__ (self):
        return self.album_title



class song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE,null=True, default = None)
    title_name= models.CharField(max_length=100)
    title = models.FileField()
    is_favorite= models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:detail',kwargs={'pk':self.album_id})


    def __str__(self):
        return self.title_name

class FriendRequest(models.Model):
    from_user_id = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default = None, related_name='from_user_id')
    to_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='to_user_id')
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, blank=True)