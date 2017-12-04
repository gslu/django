# -*- coding:utf-8 -*-
from django.conf.urls import url
from views import *
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'login/$',obtain_jwt_token),
    url(r'users/$', UserList.as_view(), name='user-list'),
    url(r'user/(?P<id>\d+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'register/$',UserCreate.as_view(),name="register"),
    url(r'posts/$', PostList.as_view(), name='post-list'),
    url(r'profile/(?P<id>\d+)/$', ProfileDetail.as_view(), name='user-profile'),
    url(r'post/(?P<id>\d+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'comments/$', CommentList.as_view(), name='comment-list'),
]