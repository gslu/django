# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from uuslug import slugify
from system.storage import ImageStorage

# Create your models here.

class Book(models.Model):
    user = models.ForeignKey(User,related_name="books")
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{}-{}'.format(self.user.username,self.name)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    hometown = models.CharField(verbose_name=u"家乡",max_length=20,blank=True)
    address = models.CharField(verbose_name=u"现住",max_length=20,blank=True)
    occupation = models.CharField(verbose_name=u"职业",max_length=20,blank=True)
    hobby = models.CharField(verbose_name=u"爱好",max_length=100,blank=True)

    nickname = models.CharField(verbose_name=u"昵称",max_length=10,blank=True,default="未名")

    GENDER_CHOICES = (
        (u'M', u'男'),
        (u'F', u'女'),
        (u'S',u'保密'),
    )
    gender = models.CharField(verbose_name=u"性别",max_length=10,choices=GENDER_CHOICES,default='S')
    motto = models.CharField(verbose_name=u"座右铭",max_length=30,blank=True,default="色即是空，空即是色")
    introduce = models.TextField(verbose_name=u"个人简介",max_length=200,blank=True)
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
    book = models.ForeignKey(Book,related_name='posts',default=None,blank=True)
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

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args,**kwargs)


class PostClass(models.Model):
    user = models.ForeignKey(User,related_name="classes",default=None)
    post = models.OneToOneField(Post,on_delete=models.CASCADE)

    STATUS_CHOICES = (
                    ('self', '原创'),
                    ('reprint', '转载'),
                    ('collect', '收藏'))
    post_type = models.CharField(max_length=10, choices=STATUS_CHOICES, default='self')

    def __unicode__(self):
        return self.post_type


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',default=None,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='comments',default=None)
    body = models.TextField(max_length=800,verbose_name="内容")
    floor = models.IntegerField(verbose_name="楼层",default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '{} 对 {} 的评论'.format(self.user,self.post)


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
        return '{0}-{1}'.format(self.email, self.send_type)


class AccessRecord(models.Model):
    master = models.ForeignKey(User,related_name='access_records')
    guest = models.ForeignKey(User,related_name="visit_records")
    access_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{} {} 访问 {}".format(self.access_time,self.guest,self.master)


class MessageRecord(models.Model):
    sender = models.ForeignKey(User,related_name='send_msg')
    receiver = models.ForeignKey(User,related_name="receive_msg")
    body = models.CharField(max_length=300, verbose_name=u"留言")
    send_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "{} {} 给 {} 留言".format(self.send_time,self.sender,self.receiver)