# -*- coding:utf-8 -*-
from django import template
from django.db.models import Count
from taggit.models import Tag
from ..models import Post,PostClass

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




