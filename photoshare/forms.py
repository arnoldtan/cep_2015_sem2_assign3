from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

class CreatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('photo', 'description')

class UpdatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('description',)

class CreateCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment',)