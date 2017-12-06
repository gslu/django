# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.hashers import  make_password
from django.utils import timezone
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser,IsAuthenticated,AllowAny
from permissions import IsOwnerOrReadOnly
from serializers import *
from blog.models import User,Profile,Post,Comment
from blog.utils import email_send

# Create your views here.

class PostList(generics.ListCreateAPIView):
    '''post list'''
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        data = request.data.copy()
        instance = self.get_object()
        ret = {"success":True,"status": 0, "msg": ""}

        if data.get("status",'') == 'published':
            data.update({"publish":timezone.now()})
        else:
            data.update({"publish": instance.publish})

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        ret.update({"data": dict(list(serializer.data.items()))})

        return Response(ret, status=status.HTTP_201_CREATED)


class UserList(generics.ListCreateAPIView):
    '''user list only access to admin'''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,IsAdminUser)


class UserCreate(generics.CreateAPIView):
    '''new user'''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        username = data.get("username", None)
        ret = {"success":True,"status": 0, "msg": ""}

        if User.objects.filter(username=username).exists():
            ret = {"success":False,"status":1,
                   "msg":"username '{}' is exists!".format(username)}
            return Response(ret, status=status.HTTP_201_CREATED)
        else:
            data.update({u"password":make_password(data.get("password"))})
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            try:
                email_send.sendVerifyEmail(data.get("email"), data.get("username"),
                                            send_type="register", request=request)
            except:
                ret = {"success":False,"status":2,"msg":"Sending mail failure!"}
            else:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
            ret.update({"data":dict(list(serializer.data.items()))})
            return Response(ret, status=status.HTTP_201_CREATED, headers=headers)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        data = request.data.copy()
        username = data.get("username", None)
        instance = self.get_object()
        ret = {"status": "success", "msg": ""}

        if username <> instance.username and User.objects.filter(username=username).exists():
            ret = {"status": "error",
                       "msg": "username '{}' is exists!".format(username)}
        else:
            data.update({u"password": make_password(data.get("password"))})
            serializer = self.get_serializer(instance,data=data,partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            ret.update({"data": dict(list(serializer.data.items()))})

        return Response(ret, status=status.HTTP_201_CREATED)





class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()



