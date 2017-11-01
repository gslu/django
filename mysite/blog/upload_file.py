# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import datetime
import uuid
import os

def handle_uploaded_file(file,dest_path):
    with open(dest_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

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
        upload_info = {"success": False, 'file_path': None}
    upload_info = json.dumps(upload_info)

    return HttpResponse(upload_info, content_type="application/json")
