"""assign3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from photoshare import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.Index.as_view()),

    url(r'^account/register$', views.UserRegister.as_view()),
    url(r'^account/login$', views.UserLogin.as_view()),
    url(r'^account/logout$', views.UserLogout.as_view()),

    url(r'^user/profile$', views.UserProfile.as_view()),
    url(r'^user/(?P<userpk>\d{1,10})/$', views.UserView.as_view()),

    url(r'^post/(?P<postpk>\d{1,10})/$', views.PostView.as_view()),
    url(r'^post/create$', views.CreatePostView.as_view()),
    url(r'^post/update/(?P<postpk>\d{1,10})/$', views.UpdatePostView.as_view()),
    url(r'^post/delete/(?P<postpk>\d{1,10})/$', views.DeletePostView.as_view()),

    url(r'^comment/create$', views.CreateCommentView.as_view()),
    url(r'^comment/update/(?P<commentpk>\d{1,10})/$', views.UpdateCommentView.as_view()),
    url(r'^comment/delete/(?P<commentpk>\d{1,10})/$', views.DeleteCommentView.as_view()),

    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),

    url(r'^community$', views.CommunityView.as_view()),
]