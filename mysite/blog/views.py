# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from .models import Post,Comment,EmailVerifyRecord
from .forms import EmailPostForm,CommentForm,LoginForm,RegisterForm,ForgetForm

from utils import email_send


# Create your views here.


def userLogin(request):

    login_status = None
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                login_status = 200

                return HttpResponseRedirect(request.session['login_from'])
            else:
                login_status = 400
                form = LoginForm(initial={"username": cd["username"],
                                                "password": cd["password"]})

    else:
        # 获取不到,则跳转到个人中心，用/user/1/暂时充当
        referer = request.META.get('HTTP_REFERER','/user/1')
        if 'register' not in referer:
            request.session['login_from'] = referer
        else:
            request.session['login_from'] = '/user/1'

        form = LoginForm()

    return render(request,"blog/login.html",{"form":form,
                                             "login_status":login_status,
                                             "type":"login"})

@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def userRegister(request):
    register_msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd["username"])
            except:
                user = None

            if user is None:
                try:
                    User.objects.create(username=cd["username"],
                                        password=make_password(cd["password"],None,"pbkdf2_sha256"),
                                        email=cd["email"],
                                        is_active=0)
                except Exception as e:
                    if settings.DEBUG:
                        register_msg = e.message
                    else:
                        register_msg = "Server error"
                else:
                    return HttpResponseRedirect(reverse("verify_register_before",
                                                        kwargs={"username":cd["username"],
                                                                "email":cd["email"]}))
            else:
                register_msg="该帐号已被注册"
                form = RegisterForm(initial={"username": cd["username"],
                                                "password": cd["password"],
                                                 "email":cd["email"]})

    else:
        form = RegisterForm()

    return render(request,"blog/login.html",{"form":form,
                                             "register_msg":register_msg,
                                             "type": "register"})

def postList(request,user_id,tag_slug=None):

    user = get_object_or_404(User,id=user_id)
    object_list = Post.published.filter(author=user)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts': posts,
                                                 'page':page,
                                                 'tag':tag,
                                                 'user':user,
                                                 'auth_user':request.user})


def postDetail(request,year,month,day,slug,id):
    post = get_object_or_404(Post, slug=slug,status='published',publish__year=year,
                                    publish__month=month, #要setting设置USE_TZ=False,否则不识别month,day
                                    publish__day=day,
                                    id=id
                                )
    if post:
        post.accesstimes += 1
        post.save()

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        #A comment was post
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return render(request,'blog/post/detail.html',{'post': post,
                                                   'comments':comments,
                                                   'comment_form':comment_form,
                                                   'new_comment':new_comment,
                                                   'similar_posts':similar_posts,
                                                   'user': post.author,
                                                   'auth_user': request.user
                                                   })
@login_required
def postShare(request,post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    cd = None
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        # Form fields passed validation
        if form.is_valid():
            cd = form.cleaned_data
            #....send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            share_from = request.user.profile.nickname
            subject = '{}　给你分享 "{}"'.format(share_from,post.title)
            message = '阅读文章 "{}" 链接 {}\n\n{} 读后感: {}'.format(post.title,
                                                                    post_url,
                                                                    share_from,cd['comments'])

            msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,[cd['to']])
            msg.content_subtype = "html"
            msg.send()
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form,'post':post,
                                                  'sent':sent,'cd':cd,
                                                  'user': post.author,
                                                  'auth_user': request.user
                                                  })


def music(request,user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request,'blog/music/music.html',{'user': user,
                                                   'auth_user': request.user})


def about(request,user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request,'blog/about/about.html',{'user': user,
                                                   'auth_user': request.user})

def verifyRegister(request,email=None,username=None,code=None):
    # False表示激活前,True表示激活后
    status = "error"
    if email is not None and username is not None:
        email_send.sendVerifyEmail(email,username,send_type="register")
        status = False

    if code is not None:
        record = get_object_or_404(EmailVerifyRecord,code=code)
        user = get_object_or_404(User,email=record.email)
        user.is_active = True
        user.save()
        EmailVerifyRecord.objects.get(code=code).delete()
        status = True
    return render(request,"blog/verify.html",{"send_type":"register",
                                              "status":status,
                                              "username":username,
                                              "email":email})

def forget(request):
    # False表示找回前,True表示找回后
    status = False
    error = False
    if request.method == 'POST':
        form = ForgetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd["username"])
            except:
                error = True
            else:
                if user.email<>cd["email"]:
                    error = True

            if error:
                form = ForgetForm(initial={"username":cd["username"],
                                           "email":cd["email"]})
            else:
                status = True

    else:
        form = ForgetForm()
    return render(request,"blog/verify.html",{"send_type":"forget",
                                              "status":status,
                                              "form":form,
                                              "error":error})



