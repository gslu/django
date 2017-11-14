# -*- coding:utf-8 -*-
from django import template
from django.db.models import Count
from django.conf import settings
from taggit.models import Tag
from ..models import Post,PostClass,UserRelation
import os,json

register = template.Library()

@register.simple_tag
def total_posts(user=None):
    return Post.published.filter(author=user).count()

@register.assignment_tag
def get_latest_posts(user=None,count=5):
    latest_posts = Post.published.filter(author=user).order_by('-publish')[:count]
    return latest_posts

@register.assignment_tag
def get_most_commented_posts(user=None,count=5):
    #聚合函数，按comments聚合后排序
    return Post.published.filter(author=user).annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.assignment_tag
def get_most_access_posts(user=None,count=5):
    most_access_posts = Post.published.filter(author=user).order_by('-accesstimes')[:count]
    return most_access_posts

@register.assignment_tag
def get_comments_count(post=None):
    comments_count = 0
    comments_count = post.comments.filter(active=True).count
    return comments_count

@register.assignment_tag
def get_tags(user=None):
    posts = Post.published.filter(author=user)
    tags = Tag.objects.filter(post__in=posts).distinct()
    return tags

@register.assignment_tag
def get_hot_tags(count=5):
    return Tag.objects.all().annotate(
        total_posts=Count('post')
    ).order_by('-total_posts')[:count]


@register.assignment_tag
def post_count(user=None,post_type=None):
    return PostClass.objects.filter(user=user,post_type=post_type).count()


@register.assignment_tag
def get_text(post_body=None):
    import re
    pattern = re.compile(r'<[^>]+>|&nbsp;', re.S)
    text = pattern.sub('',post_body)
    return text


@register.assignment_tag
def is_follower(auth_user=None,user=None):
    try:
        user_relation = UserRelation.objects.get(user=user,follower=auth_user)
    except:
        return False
    else:
        return True


@register.assignment_tag
def get_follower_count(user=None):
    return UserRelation.objects.filter(user=user).count()


@register.assignment_tag
def get_uv():
    uv = 0
    path = os.path.join(settings.BASE_DIR,'logs/nginx/uv_pv.json')
    with open(path,'r') as f:
        obj = json.load(f)
        uv = obj['uv']
    return uv


@register.assignment_tag
def get_pv():
    pv = 0
    path = os.path.join(settings.BASE_DIR,'logs/nginx/uv_pv.json')
    with open(path,'r') as f:
        obj = json.load(f)
        pv = obj['pv']
    return pv





