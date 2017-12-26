#-*- coding:utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post ,Comment,Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login','date_joined','is_superuser','is_active',
                            'is_staff','user_permissions','groups')
        extra_kwargs = {
            'username': {"required":True},
            'password': {'write_only': True,"required":True},
            'email': {"required":True},
            'is_active': {"default":False},
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
    body = serializers.CharField(allow_blank=True)
    class Meta:
        model = Post
        fields = '__all__'
        #read_only_fields = ('publish','slug')



class CommentSerializer(serializers.ModelSerializer):
    post = serializers.HyperlinkedRelatedField(view_name='api:post-detail',
                                               lookup_field='id',read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail',
                                               lookup_field='id',read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'




