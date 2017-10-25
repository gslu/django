# -*- coding:utf-8 -*-
from django import template
from django.db.models import Count
from ..models import Post

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
