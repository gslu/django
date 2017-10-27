# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from system.storage import ImageStorage

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name=u"昵称",max_length=10,blank=True,default=u"未名")

    GENDER_CHOICES = (
        (u'M', u'男'),
        (u'F', u'女'),
        (u'S',u'保密'),
    )
    gender = models.CharField(verbose_name=u"性别",max_length=10,choices=GENDER_CHOICES,default='S')
    motto = models.CharField(verbose_name=u"座右铭",max_length=50,blank=True,default="色即是空，空即是色")
    introduce = models.TextField(verbose_name=u"个人简介",max_length=300,blank=True)
    phone = models.CharField(verbose_name=u"手机",max_length=30,blank=True)
    image = models.ImageField(verbose_name=u"头像",upload_to="image/user_img",
                              blank=True,storage=ImageStorage())
    bgimg = models.ImageField(verbose_name=u"背景", upload_to="image/bg_img",
                              blank=True, storage=ImageStorage())

    def __unicode__(self):
        return self.user.username


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    STATUS_CHOICES = (
                    ('draft', 'Draft'),
                    ('published', 'Published'),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags = TaggableManager()
    accesstimes = models.IntegerField(default=0)

    class Meta:
        ordering = ('-publish',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug,
                             self.id])


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=60, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")

    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10, choices=(("register",u"注册"), ("forget",u"密码找回")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", auto_now_add=True)

    class Meta:
        verbose_name = u"VerifyRecord"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)