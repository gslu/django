# -*- coding:utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'users/$', UserList.as_view(), name='user-list'),
    url(r'user/(?P<id>\d+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'user/new/$',UserCreate.as_view(),name="create-user"),
    url(r'posts/$', PostList.as_view(), name='post-list'),
    url(r'profile/(?P<id>\d+)/$', ProfileDetail.as_view(), name='user-profile'),
    url(r'post/(?P<id>\d+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'comments/$', CommentList.as_view(), name='comment-list'),
]