# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from blog.models import PictureRecord
from .forms import *
import json,os

@login_required
@csrf_exempt
def uploadImage(request):

    file = request.FILES.get('fileData')  # 得到文件对象
    form = ArticleImageForm(request.POST,{"picture":file})
    if form.is_valid():
        pic = PictureRecord.objects.create(user=request.user, picture=form.cleaned_data["picture"])
        upload_info = {"success": True, 'file_path': pic.picture.url}
    else:
        upload_info = {"success": False, 'file_path': None,"msg":"文件上传失败"}
    upload_info = json.dumps(upload_info)

    return HttpResponse(upload_info, content_type="application/json")


@login_required
def addImage(request):
    if request.method == "POST":
        upf = get_object_or_404(Profile, user=request.user)
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            upf.image = form.cleaned_data["image"]
            upf.save()
        ret = json.dumps({"path":"{}".format(upf.image.url)})
    else:
        ret = json.dumps({"path":"error"})
    return HttpResponse(ret, content_type="application/json")


@login_required
def addBgimg(request):
    if request.method == "POST":
        upf = get_object_or_404(Profile, user=request.user)
        form = BgimgForm(request.POST,request.FILES)
        if form.is_valid():
            upf.bgimg = form.cleaned_data["bgimg"]
            upf.save()
        ret = json.dumps({"path":"{}".format(upf.bgimg.url)})
    else:
        ret = json.dumps({"path":"error"})
    return HttpResponse(ret, content_type="application/json")
