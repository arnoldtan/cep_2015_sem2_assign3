from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from slugify import slugify

from .forms import CreateUserForm
from .forms import CreatePostForm
from .forms import CreateCommentForm

from .models import Post
from .models import Comment
from .models import Follower
from django.contrib.auth.models import User

import helper
from PIL import Image

# Create your views here.
class Index(View):
	def get(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/user/' + str(request.user.pk))
		else:
			return render(request, "index/index.html", {})


class UserRegister(View):
	def post(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/user/' + str(request.user.pk))
		else:
			user_form = CreateUserForm(data=request.POST)
			if user_form.is_valid():
				user = user_form.save()

				user = authenticate(username=request.POST['username'],
														password=request.POST['password1'])

				if user is not None:
					if user.is_active:
						login(request, user)
						return HttpResponseRedirect('/user/profile')
			else:
				errors = user_form.errors
				error_string = ""
				for error in errors.values():
					error_string += slugify(error.as_text()) + '\n'
					'''encode('ascii', 'ignore'))'''
				return HttpResponseRedirect('/?' + error_string + '#signupform')

class UserLogin(View):
	def post(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/user/' + str(request.user.pk) + '/')
		else:
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/user/profile')
				else:
					return HttpResponseRedirect('/?' + 'disabled-account\n' + '#loginform')
			else:
				return HttpResponseRedirect('/?' + 'invalid-login\n' + '#loginform')

class UserLogout(View):
	@method_decorator(login_required)
	def get(self, request):
		logout(request)
		return HttpResponseRedirect('/')

class UserProfile(View):
	@method_decorator(login_required)
	def get(self, request):
		return HttpResponseRedirect('/user/' + str(request.user.pk) + '/')

class UserView(View):
	@method_decorator(login_required)
	def get(self, request, userpk):
		user = request.user
		user_profile = User.objects.get(pk=userpk)
		posts = Post.objects.all().filter(user=user_profile).order_by('date').reverse()
		followers = Follower.objects.all().filter(followed=user_profile, accepted=True)
		following = Follower.objects.all().filter(follower=user_profile, accepted=True)
		if int(str(userpk)) != request.user.pk:
			allowed = Follower.objects.all().filter(followed=user_profile, follower=user, accepted=True)
			if not allowed:
				return render(request, "user/user_protected.html", {
					'user': user_profile,
					'posts': posts,
					'followers': followers,
					'following': following,
					'num_posts': len(posts),
					'num_followers': len(followers),
					'num_following': len(following)
				})
			else:
				return render(request, "user/user_profile.html", {
					'user_profile': user_profile,
					'posts': posts,
					'followers': followers,
					'following': following,
					'num_posts': len(posts),
					'num_followers': len(followers),
					'num_following': len(following),
					'owner': False
				})
		else:
			return render(request, "user/user_profile.html", {
				'user_profile': user_profile,
				'posts': posts,
				'followers': followers,
				'following': following,
				'num_posts': len(posts),
				'num_followers': len(followers),
				'num_following': len(following),
				'owner': True
			})

class CreatePostView(View):
	@method_decorator(login_required)
	def post(self, request):
		create_post_form = CreatePostForm(request.POST, request.FILES)
		if create_post_form.is_valid():
			post = create_post_form.save(commit=False)
			post.user = request.user
			post.save()
			return HttpResponseRedirect('/post/' + str(post.pk) + '/')

class UpdatePostView(View):
	@method_decorator(login_required)
	def post(self, request, postpk):
		post = Post.objects.get(pk=postpk)
		if post.user == request.user:
			post.description = request.POST['description']
			post.save()
			return HttpResponseRedirect('/post/' + str(post.pk))
		else:
			return HttpResponse("<h1>You do not have permission to perform this action</h1>", status_code=403)

class DeletePostView(View):
	@method_decorator(login_required)
	def post(self, request, postpk):
		post = Post.objects.get(pk=postpk)
		if post.user == request.user:
			post.delete()
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("<h1>You do not have permission to perform this action</h1>", status_code=403)

class PostView(View):
	@method_decorator(login_required)
	def get(self, request, postpk):
		post = Post.objects.get(pk=postpk)
		comments = Comment.objects.all().filter(post=post).order_by('date').reverse()
		if post.user == request.user:
			print('got')
			return render(request, "post/edit_post.html", {
				'post': post,
				'comments': comments
			})
		else:
			return render(request, "post/post.html", {
				'post': post,
				'comments': comments
			})

class CreateCommentView(View):
	@method_decorator(login_required)
	def post(self, request):
		create_comment_form = CreateCommentForm(data=request.POST)
		post = Post.objects.get(pk=request.POST['postpk'])
		if create_comment_form.is_valid():
			comment = create_comment_form.save(commit=False)
			comment.user = request.user
			comment.post = post
			comment.save()
			return HttpResponseRedirect('/post/' + str(post.pk) + '#comment_' + str(comment.pk))

class UpdateCommentView(View):
	@method_decorator(login_required)
	def post(self, request, commentpk):
		comment = Comment.objects.get(pk=commentpk)
		post = Post.objects.get(comment=comment)
		if comment.user == request.user:
			comment.comment = request.POST['comment']
			comment.save()
			return HttpResponseRedirect('/post/' + str(post.pk) + '#comment_' + str(comment.pk))
		else:
			return HttpResponse("<h1>You do not have permission to perform this action</h1>", status_code=403)
		return HttpResponseRedirect(request.path)

class DeleteCommentView(View):
	@method_decorator(login_required)
	def post(self, request, commentpk):
		comment = Comment.objects.get(pk=commentpk)
		post = Post.objects.get(comment=comment)
		if comment.user == request.user:
			comment.delete()
			return HttpResponseRedirect('/post/' + str(post.pk))
		else:
			return HttpResponse("<h1>You do not have permission to perform this action</h1>", status_code=403)

class CommunityView(View):
	@method_decorator(login_required)
	def get(self, request):
		user = request.user
		posts = Post.objects.all().filter(user=user).order_by('date').reverse()
		followers = Follower.objects.all().filter(followed=user, accepted=True)
		following = Follower.objects.all().filter(follower=user, accepted=True)
		follow_requests = Follower.objects.all().filter(followed=user, accepted=False)
		following_requests = Follower.objects.all().filter(follower=user, accepted=False)
		exclude_userpk = [o.followed.pk for o in following]
		exclude_user = [o.followed for o in following]
		overlap = followers.exclude(followed__in=exclude_user)
		exclude_userpk += [o.followed.pk for o in overlap]
		exclude_userpk += [ user.pk ]
		exclude_userpk += [o.followed.pk for o in following_requests]
		other_users = User.objects.all().exclude(pk__in=exclude_userpk)
		return render(request, "community/community.html", {
			'user': user,
			'posts': posts,
			'followers': followers,
			'following': following,
			'follow_requests': follow_requests,
			'other_users': other_users,
			'following_requests': following_requests,
			'num_posts': len(posts),
			'num_followers': len(followers),
			'num_following': len(following),
			'num_follow_requests': len(follow_requests),
			'num_other_users': len(other_users) + len(following_requests),
		})

class AddFollowView(View):
	@method_decorator(login_required)
	def get(self, request, userpk):
		follower = request.user
		followed = User.objects.get(pk=userpk)
		follow_model = Follower.objects.all().filter(followed=followed, follower=follower)
		if not follow_model:
			follow = Follower(followed=followed, follower=follower, accepted=False)
			follow.save()
			return HttpResponseRedirect('/community')
		else:
			return HttpResponseRedirect('/community')


class AcceptFollowView(View):
	@method_decorator(login_required)
	def get(self, request, userpk):
		followed = request.user
		follower = User.objects.get(pk=userpk)
		follow_model = Follower.objects.get(followed=followed, follower=follower)
		if not follow_model:
			return HttpResponseRedirect('/community')
		else:
			if follow_model.accepted == True:
				return HttpResponseRedirect('/community')
			else:
				follow_model.accepted = True
				follow_model.save()
				return HttpResponseRedirect('/community')

class RejectFollowView(View):
	@method_decorator(login_required)
	def get(self, request, userpk):
		followed = request.user
		follower = User.objects.get(pk=userpk)
		follow_model = Follower.objects.get(followed=followed, follower=follower)
		if not follow_model:
			return HttpResponseRedirect('/community')
		else:
			follow_model.delete()
			return HttpResponseRedirect('/community')

class DeleteFollowView(View):
	@method_decorator(login_required)
	def get(self, request, userpk):
		follower = request.user
		followed = User.objects.get(pk=userpk)
		follow_model = Follower.objects.get(followed=followed, follower=follower)
		if not follow_model:
			return HttpResponseRedirect('/community')
		else:
			follow_model.delete()
			return HttpResponseRedirect('/community')