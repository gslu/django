# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,View
from django.db.models import Count
from taggit.models import Tag
from .models import Post,Comment,EmailVerifyRecord,Book
from .forms import *
from utils import email_send
from django.db.models import Q

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
                try:
                    return HttpResponseRedirect(request.session['login_from'])
                except:
                    #跳转错误，跳到网站主页，由number1个人主页暂时充当
                    return HttpResponseRedirect('/')
            else:
                login_status = 400
                form = LoginForm(initial={"username": cd["username"],
                                                "password": cd["password"]})

    else:
        # 获取不到,则跳转到个人中心，用/user/1/暂时充当
        referer = request.META.get('HTTP_REFERER','/')
        print referer
        if 'register' in referer or 'login' in referer:
            request.session['login_from'] = '/'
        else:
            request.session['login_from'] = referer

        form = LoginForm()
    return render(request,"blog/user/login.html",{"form":form,
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
            username = cd["username"]
            email = cd["email"]
            password = cd["password"]

            try:
                user = User.objects.get(username=username)
            except:
                user = None

            if user is None and cd["code"] == "l14789632":
                try:
                    email_send.sendVerifyEmail(email, username,
                                               send_type="register", request=request)

                    user = User.objects.create(username=username,
                                        password=password,
                                        email=email,
                                        is_active=0)
                    user.set_password(password)
                    user.save()
                except Exception as e:
                    if settings.DEBUG:
                        register_msg = e.message
                    else:
                        register_msg = "Server error"
                else:
                    return HttpResponseRedirect(reverse("blog:verify_register_before",
                                                        kwargs={"email":email,
                                                                "username":username}))
            else:
                register_msg="暂不支持"
                #register_msg="该帐号已被注册"
                form = RegisterForm(initial={"username": cd["username"],
                                                "email":cd["email"],
                                                "password":""})

    else:
        form = RegisterForm()

    return render(request,"blog/user/login.html",{"form":form,
                                             "register_msg":register_msg,
                                             "type": "register"})


def verifyRegister(request,email=None,username=None,code=None):

    import datetime
    #验证链接一天过期
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(days=1)

    # False表示激活前,True表示激活后 error错误页
    status = "error"
    if email is not None and username is not None:
        status = False

    if code is not None:
        record = get_object_or_404(EmailVerifyRecord,code=code,send_time__gte=one_day_ago)
        user = get_object_or_404(User,email=record.email,username=username)
        user.is_active = True
        user.save()
        record.delete()
        status = True
        email = record.email
        username = user.username
    return render(request,"blog/user/verify.html",{"send_type":"register",
                                              "status":status,
                                              "username":username,
                                              "email":email})


def pswdForget(request):
    # False/True 重置邮件发送前后
    status = False
    query_error = False
    email = None
    username = None
    if request.method == 'POST':
        form = ForgetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd["username"]
            email = cd["email"]
            try:
                user = User.objects.get(username=username,email=email)
            except:
                query_error = True

            if query_error:
                form = ForgetForm(initial={"username":username,
                                           "email":email})
            else:
                email_send.sendVerifyEmail(email, username, send_type="forget",request=request)
                status = True
    else:
        form = ForgetForm()
        username = None
    return render(request,"blog/user/verify.html",{"send_type":"forget",
                                              "status":status,"email":email,
                                              "form":form,"username":username,
                                              "error":query_error})


def pswdReset(request,username,code):
    import datetime
    #重置密码链接一天过期
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(days=1)
    record = get_object_or_404(EmailVerifyRecord,code=code,send_time__gte=one_day_ago)
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if username == cd["username"]:
                user = get_object_or_404(User, username=username, email=record.email)
                user.set_password(cd["password"])
                user.save()
                record.delete()
                form = None
            else:
                form = ResetForm(initial={"username": username})
    else:
        form = ResetForm(initial={"username":username})
    return render(request,"blog/user/reset.html",{"form":form})


def updateAccessRecord(request,user):
    if not request.user.is_authenticated:
        return
    elif request.user == user:
        return
    else:
        try:
            import datetime
            record = request.user.visit_records.get(master=user)
            record.access_time = datetime.datetime.now()
            record.save()
        except:
            request.user.visit_records.create(master=user)


def postList(request,user_id, tag_name=None):

    user = get_object_or_404(User,id=user_id)
    updateAccessRecord(request, user)
    object_list = Post.published.filter(author=user)
    tag = None
    tags = Tag.objects.filter(post__in=object_list).distinct()

    if tag_name:
        tag = get_object_or_404(Tag,name=tag_name)
        tags = tags.filter(~Q(name=tag))
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
                                                 'tag':tag,
                                                 'tags':tags,
                                                 'user':user,
                                                 'auth_user':request.user})


def postDetail(request,year,month,day,slug,id):
    post = get_object_or_404(Post, slug=slug,status='published',publish__year=year,
                                    publish__month=month, #要setting设置USE_TZ=False,否则不识别month,day
                                    publish__day=day,
                                    id=id)
    if post:
        post.accesstimes += 1
        post.save()

    comments = post.comments.filter(active=True).order_by("created")
    new_comment = None
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                if comments:
                    new_comment.floor = comments.count() + 1
                else:
                    new_comment.floor = 1
                new_comment.save()
                comments = post.comments.filter(active=True).order_by("created")
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    if new_comment:
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


def about(request,user_id,option):
    if option not in ("ps","ra","rc","rm"):
        return Http404
    user = get_object_or_404(User, id=user_id)

    def getPageAndObjs(obj,per_page):
        paginator = Paginator(obj,per_page)
        page = request.GET.get('page')
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)
        return (page,objs)


    if option == "ra":
        ra = user.access_records.order_by('access_time')
        page,ra = getPageAndObjs(ra,27)
    else:
        ra = None

    if option == "rc":
        posts = Post.objects.filter(author=user)
        rc = Comment.objects.filter(post__in=posts).order_by("updated")
        page, rc = getPageAndObjs(rc, 10)
    else:
        rc = None

    if option == "rm":
        rm = user.receive_msg.order_by("send_time")
        page, rm = getPageAndObjs(rm, 15)
    else:
        rm = None

    return render(request,'blog/about/about.html',{'user': user,
                                                   'auth_user': request.user,
                                                   "option":option,
                                                   "ra":ra,"rc":rc,"rm":rm})

@login_required
def writePost(request):
    post = Post.objects.create(title="无标题文章", status="draft", body="",author=request.user)
    return HttpResponseRedirect(reverse("blog:edit_post", kwargs={"post_id": post.id}))


@login_required
def editPost(request,post_id=None,opt=None):

    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = WriteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post.title=cd["title"]
            if opt == "publish":
                post.status="published"
            else:
                post.status = "draft"
            post.body = cd["body"]
            post.save()
            return HttpResponseRedirect(reverse("blog:edit_post", kwargs={"post_id": post.id}))
    else:
        form = WriteForm(initial={"title":post.title,"body": post.body,})

    return render(request,"blog/edit/write.html",{"form":form,"auth_user":request.user, "post_id":post_id})


@login_required
def postManage(request,book_id=None,tag_name=None,post_id=None):
    books = Book.objects.filter(user=request.user).order_by('created')
    if book_id is not None:
        point_book = get_object_or_404(Book,id=book_id)
    else:
        point_book = books[0]
    tags = Tag.objects.filter(post__in=point_book.posts.all()).distinct()

    if tag_name is not None:
        point_tag = get_object_or_404(Tag, name=tag_name)
    else:
        point_tag = tags[0]

    posts = Post.objects.filter(author=request.user,tags=point_tag)

    return render(request,"blog/edit/manage.html",{"books":books,
                                                   "tags":tags,
                                                   "posts": posts,
                                                   "point_book":point_book,
                                                   "point_tag":point_tag,
                                                   "auth_user":request.user})

