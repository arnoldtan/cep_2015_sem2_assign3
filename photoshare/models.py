from django.db import models
from django.contrib.auth.models import User
from django import forms
import os
from django.core.files.storage import FileSystemStorage

# Create your models here.
fs = FileSystemStorage(location=os.getcwd() + '/photoshare/uploads/photos')

class Post(models.Model):
	user = models.ForeignKey(User, related_name="posts")
	likes = models.ManyToManyField(User, related_name="likes")

	photo = models.ImageField(upload_to="photos/%Y/%m/%d", max_length=1000)
	description = models.CharField(max_length=1000)
	date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)

	comment = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
	follower = models.ForeignKey(User, related_name="following")
	followed = models.ForeignKey(User, related_name="followers")

	accepted = models.BooleanField(default=None)