# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from django.utils import timezone
from taggit.models import Tag
from .models import Post,Comment,VerifyRecord,Book,PictureRecord,UserRelation,Collection,Pv
from .forms import *
from utils import email_send
from django.db.models import Q
import json

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

            if User.objects.filter(username=username).exists():
                register_msg = "该帐号已被使用"
            elif User.objects.filter(email=email).exists():
                register_msg = "该邮箱已注册"
            else:
                try:
                    email_send.sendVerifyEmail(email, username,
                                               send_type="register", request=request)
                    user = User.objects.create(username=username,password=password,
                                        email=email,is_active=0)
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
        record = get_object_or_404(VerifyRecord,code=code,send_time__gte=one_day_ago)
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
    record = get_object_or_404(VerifyRecord,code=code,send_time__gte=one_day_ago)
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
    return render(request,"blog/user/reset.html",{"form":form,"type":"reset"})


@login_required
def pswdChange(request):
    if request.method == 'POST':
        form = PswdChangeForm(request.user,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_password = cd["password_confirm"]
            request.user.set_password(new_password)
            request.user.save()
            form = None
    else:
        form = PswdChangeForm(request.user)
    return render(request,"blog/user/reset.html",{"form":form,"type":"change"})



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
    object_list = Post.published.filter(author=user).annotate(
                    total_comments=Count('comments')
                ).order_by('-total_comments')
    tag = None
    tags = Tag.objects.filter(post__in=object_list).distinct()

    if tag_name:
        tag = get_object_or_404(Tag,name=tag_name)
        tags = tags.filter(~Q(name=tag))
        object_list = object_list.filter(tags__in=[tag])

    # 8 posts in each page
    paginator = Paginator(object_list, 8)
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

    # get cache
    cache_key = "post:{}".format(id)
    if cache.has_key(cache_key):
        post = cache.get(cache_key)
    else:
        post = get_object_or_404(Post, slug=slug,status='published',created__year=year,
                                    created__month=month, #要setting设置USE_TZ=False,否则不识别month,day
                                    created__day=day,
                                    id=id)
        cache.set(cache_key,post,3600)

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
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    cd = None
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            share_from = request.user.profile.nickname
            subject = '{}　给你分享 "{}"'.format(share_from,post.title)
            message = '阅读文章 "{}" 链接 {}<br/><br/>{} 读后感: {}'.format(post.title,
                                                                    post_url,
                                                                    share_from,cd['comments'])

            email_send.sendEmail(subject, message, settings.DEFAULT_FROM_EMAIL,[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form,'post':post,
                                                  'sent':sent,'cd':cd,
                                                  'user': post.author,
                                                  'auth_user': request.user
                                                  })


def log(request,user_id,year=None,month=None):
    user = get_object_or_404(User, id=user_id)
    dates = Post.published.filter(author=user.id).order_by('-created').values_list("created")
    dates = [date[0] for date in dates]
    if dates == []:
        posts = None
        y = 0
        m = 0
    else:
        y = year if year else dates[0].year
        m = month if month  else dates[0].month
        posts = Post.published.filter(author=user,created__year=y,created__month=m)
    return render(request,'blog/log/log.html',{'user': user,
                                               'auth_user': request.user,
                                               'dates':dates,
                                               'posts':posts,
                                               'select_y':int(y),
                                               'select_m':int(m)})
def follow(request,user_id):
    user = get_object_or_404(User, id=user_id)
    dates = Post.published.filter(author=user.id).values_list("publish")
    dates = [date[0] for date in dates]
    follows = UserRelation.objects.filter(follower=user).order_by("-follow_time")
    select = "follow"
    return render(request,'blog/log/log.html',{'user': user,
                                               'auth_user': request.user,
                                               'dates':dates,
                                               'follows':follows,
                                               'select':select})
def collection(request,user_id):
    user = get_object_or_404(User, id=user_id)
    dates = Post.published.filter(author=user.id).values_list("publish")
    dates = [date[0] for date in dates]
    collections = user.collections.all().order_by('-collect_time')
    select = 'collection'
    return render(request,'blog/log/log.html',{'user': user,
                                               'auth_user': request.user,
                                               'dates':dates,
                                               'collections':collections,
                                               'select':select})


def music(request,user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request,'blog/music/music.html',{'user': user,
                                                   'auth_user': request.user})



def picture(request,user_id):
    user = get_object_or_404(User, id=user_id)
    prds = PictureRecord.objects.filter(user__id=user_id).order_by("-created")
    return render(request,'blog/picture/picture.html',{'user': user,
                                                        'auth_user': request.user,
                                                       "pictures":prds})


def about(request,user_id,option):
    if option not in ("ps","ra","rc","rm"):
        return Http404
    user = get_object_or_404(User, id=user_id)

    def getPageAndQuerySet(obj,per_page):
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
        page,ra = getPageAndQuerySet(ra,27)
    else:
        ra = None

    if option == "rc":
        posts = Post.objects.filter(author=user)
        rc = Comment.objects.filter(post__in=posts).order_by("updated")
        page, rc = getPageAndQuerySet(rc, 8)
    else:
        rc = None

    if option == "rm":
        rm = user.receive_msg.order_by("send_time")
        page, rm = getPageAndQuerySet(rm, 15)
    else:
        rm = None

    return render(request,'blog/about/about.html',{'user': user,
                                                   'auth_user': request.user,
                                                   "option":option,
                                                   "ra":ra,"rc":rc,"rm":rm})

@login_required
def writePost(request,book_id,tag_name):
    GUEST_POST_LIMIT = 5
    if not request.user.is_superuser:
        post_count = Post.objects.filter(author=request.user).count()
        if post_count >= GUEST_POST_LIMIT:
            return HttpResponse("访客文章数量限制,敬请谅解！")
    book = get_object_or_404(Book,id=book_id)
    post = Post.objects.create(title="无标题文章",book=book,
                               status="draft", body="",author=request.user)
    post.tags.add(tag_name)
    post.save()
    return HttpResponseRedirect(reverse("blog:edit_post", kwargs={"post_id": post.id}))


@login_required
def editPost(request,post_id=None,opt=None):
    post = get_object_or_404(Post, id=post_id,author=request.user)

    if request.method == "POST":
        form = WriteForm(request.POST)
        try:
            post_type = request.POST.get("post_type")
            if post_type not in ("self", "reprint"):
                return Http404
        except:
            return Http404
        if form.is_valid():
            cd = form.cleaned_data
            post.title=cd["title"]
            post.postclass.post_type = post_type
            if opt == "publish":
                post.status="published"
                post.publish = timezone.now()
            else:
                post.status = "draft"
            post.body = cd["body"]
            post.save()

            # 更新cache
            cache_key = "post:{}".format(post_id)
            if post.status == "published":
                cache.set(cache_key,post,3600)
            else:
                cache.delete_pattern(cache_key)

    else:
        form = WriteForm(initial={"title":post.title,"body": post.body,})

    return render(request,"blog/edit/write.html",{"form":form,"auth_user":request.user, "post":post})


@login_required
def newBook(request):
    if request.method == "POST":
        book_f = NewBookForm(request.POST)
        if book_f.is_valid():
            name = book_f.cleaned_data["book_name"]
            return Book.objects.get_or_create(name=name,user=request.user)
        else:
            return False,False
    else:
        return False,False

@login_required
def addTag(request,book_id):
    if request.method == "POST" and book_id is not None:
        book = get_object_or_404(Book,id=book_id)
        tag_f = NewTagForm(request.POST)
        if tag_f.is_valid():
            name = tag_f.cleaned_data["tag_name"]
            if book.tags.filter(name=name).exists():
                return get_object_or_404(book.tags,name=name),False
            else:
                book.tags.add(name)
            return get_object_or_404(book.tags,name=name),True
        else:
            return False,False
    else:
        return False,False



@login_required
def postManage(request,book_id=None,tag_name=None):

    context = {}
    point_book,new_book = newBook(request)
    point_tag,new_tag = addTag(request, book_id)
    if point_book and new_book == False:
        context["newbook_error"] = "book is exist!"
    else:
        context["newbook_error"] = ""

    if point_tag and new_tag == False:
        context["newtag_error"] = "tag is exist!"
    else:
        context["newtag_error"] = ""

    books = Book.objects.filter(user=request.user).order_by('-updated')

    if not books:
        point_book = Book.objects.create(user=request.user,name="默认")
        books = [point_book]
    else:
        if book_id is not None:
            point_book = get_object_or_404(Book,id=book_id)
        else:
            point_book = point_book if point_book else books[0]

    if not point_book.tags.all():
        point_book.tags.add("杂记")

    tags = point_book.tags.all()

    if not point_tag:
        if tag_name is None:
            point_tag = tags[0]
        else:
            point_tag = get_object_or_404(tags,name=tag_name)
    posts = Post.objects.filter(author=request.user,
                                tags__in=[point_tag],
                                book=point_book).order_by('-updated')

    context["books"] = books
    context["tags"] = tags
    context["posts"] = posts
    context["point_book"] = point_book
    context["point_tag"] = point_tag
    context["auth_user"] = request.user
    context["tag_form"] = NewTagForm()
    context["book_form"] = NewBookForm()

    return render(request,"blog/edit/manage.html",context)


@login_required
def center(request):

    image_form = ImageForm()
    bgimg_form = BgimgForm()

    basic_form = BasicForm(instance=request.user.profile)
    person_form = PersonForm(instance=request.user.profile)
    phone_form = PhoneForm(instance=request.user.profile)
    email_form = EmailForm(instance=request.user)

    context = {}
    context["image_form"] = image_form
    context["bgimg_form"] = bgimg_form
    context["auth_user"] = request.user
    context["basic_form"] = basic_form
    context["person_form"] = person_form
    context["phone_form"] = phone_form
    context["email_form"] = email_form
    return render(request, "blog/edit/center.html", context)


@login_required
def settingSave(request):

    ret = json.dumps({"status": "error"})
    if request.method == "POST":
        basic_form = BasicForm(request.POST)
        person_form = PersonForm(request.POST)
        phone_form = PhoneForm(request.POST)
        email_form = EmailForm(request.POST)
        if basic_form.is_valid() and person_form.is_valid() and\
            phone_form.is_valid() and email_form.is_valid():
            request.user.profile.__dict__.update(basic_form.cleaned_data)
            request.user.profile.__dict__.update(person_form.cleaned_data)
            request.user.profile.__dict__.update(phone_form.cleaned_data)
            request.user.email = email_form.cleaned_data["email"]
            request.user.save()
            ret = json.dumps({"status": "success"})
    return HttpResponse(ret, content_type="application/json")


# post manage

@login_required
@csrf_exempt
def bookReName(request):

    ret = json.dumps({"status": "error"})
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        new_name = request.POST.get("new_name")

        if Book.objects.filter(name=new_name,user=request.user).exists():
            ret = json.dumps({"status": "exist","msg":"new name is exists"})
        else:
            book = get_object_or_404(Book,id=book_id,user=request.user)
            book.name = new_name
            book.save()
            ret = json.dumps({"status": "success"})
    return HttpResponse(ret, content_type="application/json")


@login_required
@csrf_exempt
def tagReName(request):
    ret = json.dumps({"status": "error"})
    if request.method == "POST":
        tag_name = request.POST.get("tag_name")
        book_id = request.POST.get("book_id")
        new_name = request.POST.get("new_name")

        #if Book.objects.filter(tags__name__in=[new_name],id=book_id).exists():
        #    ret = json.dumps({"status": "exist", "msg": "new name is exists"})
        #else:
        book = get_object_or_404(Book,id=book_id,user=request.user)
        if new_name in book.tags.names():
            ret = json.dumps({"status": "exist", "msg": "new name is exists"})
        else:
            post = book.posts.all()
            post_by_tag = post.filter(tags__name__in=[tag_name])

            book.tags.remove(tag_name)
            book.tags.add(new_name)
            book.save()

            #没找到批量update tags的方法
            map((lambda post:post.tags.remove(tag_name)),post_by_tag)
            map((lambda post:post.tags.add(new_name)), post_by_tag)
            [post.save() for post in post_by_tag]

            ret = json.dumps({"status": "success"})
    return HttpResponse(ret, content_type="application/json")



@login_required
@csrf_exempt
def delBook(request):
    ret = json.dumps({"status": "success"})
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book,id=book_id,user=request.user)
        if not book.posts.all():
            book.delete()
        else:
            ret = json.dumps({"status": "error"})
    return HttpResponse(ret, content_type="application/json")


@login_required
@csrf_exempt
def delTag(request):
    ret = json.dumps({"status": "success"})
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        tag_name = request.POST.get("tag_name")
        book = get_object_or_404(Book, id=book_id, user=request.user)
        if not book.posts.filter(tags__name__in=[tag_name]):
            if book.tags.all().count() == 1:
                ret = json.dumps({"status": "lastone"})
            else:
                book.tags.remove(tag_name)
        else:
            ret = json.dumps({"status": "error"})
    return HttpResponse(ret, content_type="application/json")


@login_required
@csrf_exempt
def delPost(request):
    ret = json.dumps({"status": "success"})
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        try:
            post = Post.objects.get(id=post_id,author=request.user)
        except:
            ret = json.dumps({"status": "error"})
        else:
            post.delete()
    return HttpResponse(ret, content_type="application/json")


@login_required
@csrf_exempt
def changeTag(request):
    ret = json.dumps({"status": "success"})
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        new_tag = request.POST.get("new_tag")
        tag_name = request.POST.get("tag_name")
        try:
            post = Post.objects.get(id=post_id,author=request.user)
        except:
            ret = json.dumps({"status": "error"})
        else:
            post.tags.remove(tag_name)
            post.tags.add(new_tag)
            post.book.tags.add(new_tag)
    return HttpResponse(ret, content_type="application/json")



@login_required
@csrf_exempt
def changeBook(request):
    ret = {"status": "success","book_id":""}
    if request.method == "POST":
        tag_name = request.POST.get("tag_name")
        book_id = request.POST.get("book_id")
        new_book_name = request.POST.get("new_book_name")

        book = get_object_or_404(Book,id=book_id,user=request.user)
        (new_book,exist) = Book.objects.get_or_create(name=new_book_name,user=request.user)
        try:
            book.posts.filter(tags__name__in=[tag_name]).update(book=new_book)
            book.tags.remove(tag_name)
            new_book.tags.add(tag_name)
        except:
            ret = {"status": "error","book_id":""}

        ret["book_id"] = new_book.id

        ret = json.dumps(ret)
    return HttpResponse(ret, content_type="application/json")


@login_required
@csrf_exempt
def editFollow(request,user_id):

    ret = {"status": "follow"}
    user = get_object_or_404(User, id=user_id)
    relation,created = UserRelation.objects.get_or_create(user=user,follower=request.user)
    if not created:
        relation.delete()
        ret = {"status": "cancel-follow"}
    ret = json.dumps(ret)
    return HttpResponse(ret, content_type="application/json")


@login_required
@csrf_exempt
def editCollect(request,post_id):

    ret = {"status": "collect"}
    post = get_object_or_404(Post, id=post_id)
    collection,new = Collection.objects.get_or_create(collect_post=post,user=request.user)
    if not new:
        collection.delete()
        ret = {"status": "cancel-collect"}
    ret = json.dumps(ret)
    return HttpResponse(ret, content_type="application/json")



@csrf_exempt
def addPv(request):
    msg = {"status": "success"}
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        pv,create = Pv.objects.get_or_create(post=post)
        pv.accesstimes += 1
        pv.save()
    msg = json.dumps(msg)
    return HttpResponse(msg, content_type="application/json")