#coding:utf-8

from django.core.mail import EmailMessage
from django.conf import settings
from blog.models import EmailVerifyRecord
import uuid

def sendVerifyEmail(email,name,send_type="register"):

    code = unicode(uuid.uuid1())
    EmailVerifyRecord.objects.create(code=code,email=email,send_type=send_type)


    subject = u"浮文掠影帐号－注册激活"
    message = u"""\n\n尊敬的{}:\n您好，请点击下面的链接激活你的账号\n
                    http://127.0.0.1:8000/verify/{}""".format(name,code)

    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = "html"
    send_status = msg.send()
    return send_status









