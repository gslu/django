# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
#from .models import Profile
from .forms import *
import json
import datetime
import os,random,uuid,time

def handle_uploaded_file(file,dest_path):
    with open(dest_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

@login_required
@csrf_exempt
def uploadImage(request):

    file = request.FILES.get('fileData')  # 得到文件对象
    if file:
        today = datetime.datetime.today()
        dest_dir = settings.MEDIA_ROOT + 'article_image/'
        ext = os.path.splitext(file.name)[1]
        file_name = "{}-{}-{}-{}{}".format(today.year, today.month, today.day, uuid.uuid1(), ext)
        dest_path = "{}{}".format(dest_dir, file_name)
        handle_uploaded_file(file,dest_path)  # 上传文件
        # 得到JSON格式的返回值
        upload_info = {"success": True, 'file_path': settings.MEDIA_URL + 'article_image/'+ file_name}
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
        ret = json.dumps({"path":"{}{}".format(settings.MEDIA_URL,upf.image)})
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
        ret = json.dumps({"path":"{}{}".format(settings.MEDIA_URL,upf.bgimg)})
    else:
        ret = json.dumps({"path":"error"})
    return HttpResponse(ret, content_type="application/json")
