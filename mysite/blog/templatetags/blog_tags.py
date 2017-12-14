# -*- coding:utf-8 -*-
from django import template
from django.db.models import Count
from django.db.models import Sum
from taggit.models import Tag
from ..models import Post,PostClass,UserRelation,Pv,Collection
from collections import namedtuple
import copy

register = template.Library()

@register.assignment_tag
def get_pagination(page_data):
    pageObj = namedtuple("pageObj",['page','part_one','part_two',
                                    'part_three','part_four','part_five'])
    part_one,part_two,part_three,part_four,part_five = None,"...",None,"...",None
    if page_data.paginator.num_pages <= 6:
        part_one = range(1,page_data.paginator.num_pages+1)
    else:
        if page_data.number <= 3:
            part_one = range(1,page_data.paginator.num_pages+1)[:5]
            part_three = [page_data.paginator.num_pages]
        elif page_data.paginator.num_pages-page_data.number <= 2:
            part_one = [1]
            part_three = range(1,page_data.paginator.num_pages+1)[-5:]
        else:
            part_one = [1]
            part_three = [page_data.number-2, page_data.number-1,\
                          page_data.number, page_data.number+1, page_data.number+2]
            part_five = [page_data.paginator.num_pages]

    page = pageObj(page=page_data, part_one=part_one, part_two=part_two,
                   part_three=part_three, part_four=part_four, part_five=part_five)
    return page

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
def get_accesstimes(post=None):
    try:
        pv = Pv.objects.get(post=post)
        accesstimes = pv.accesstimes
    except:
        accesstimes = 0
    return accesstimes


@register.assignment_tag
def get_pv(user=None):
    posts = Post.objects.filter(author=user)
    pv = Pv.objects.filter(post__in=posts).aggregate(Sum('accesstimes'))
    return pv["accesstimes__sum"] if pv["accesstimes__sum"] is not None else 0


@register.assignment_tag
def get_years(dates):
    years = set([date.year for date in dates])
    years = sorted(list(years),reverse=True)
    return years

@register.assignment_tag
def get_months(dates,year):
    month_post = namedtuple('month_post', ['month', 'post_count'])
    months = [date.month for date in dates if date.year==year]
    set_months = sorted(list(set(months)),reverse=True)
    month_posts = (month_post(month=month,post_count=months.count(month)) for month in set_months)
    return month_posts


@register.assignment_tag
def is_collected(post,user):
    try:
        Collection.objects.get(collect_post=post,user=user)
    except:
        return False
    else:
        return True


@register.assignment_tag
def get_person(auth_user,user):
    if auth_user.is_authenticated() and user==auth_user:
        return "我"
    else:
        return "Ta"







