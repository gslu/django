#-*- coding:utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post ,Comment,Profile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,allow_blank=False,min_length=5,max_length=50)
    password = serializers.CharField(required=True,allow_blank=False,min_length=6,max_length=100)
    email = serializers.EmailField(required=True,allow_blank=False,max_length=50)
    is_active = serializers.BooleanField(default=False,read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login','date_joined','is_superuser','is_active',
                            'is_staff','user_permissions','groups')
        extra_kwargs = {
            'password': {'write_only': True},
        }



class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail',
                                               lookup_field='id',read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    #author = UserSerializer()
    author = serializers.HyperlinkedRelatedField(view_name='api:user-detail',
                                                 lookup_field='id',read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.HyperlinkedRelatedField(view_name='api:post-detail',
                                               lookup_field='id',read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail',
                                               lookup_field='id',read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'




