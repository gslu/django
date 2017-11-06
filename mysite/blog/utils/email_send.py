#coding:utf-8

from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from blog.models import EmailVerifyRecord
import uuid

def sendVerifyEmail(email,name,send_type="register",request=None):

    code = unicode(uuid.uuid1())

    if send_type == "register":
        subject = u"浮文掠影帐号－注册激活"
        link = request.build_absolute_uri(reverse("blog:verify_register_after",
                                                    kwargs={"code":code,"username":name}))
        message = u"""<br/>尊敬的{}:<br/>您好，请点击下面的链接激活你的账号<br/>
                    {}""".format(name,link)
    else:
        subject = u"浮文掠影帐号－密码重置"
        link = request.build_absolute_uri(reverse("blog:pswd_reset",
                                                    kwargs={"code":code,"username":name}))
        message = u"""<br/>尊敬的{}:<br/>您好，密码重置链接<br/> 
                    {} <br/>为了您的帐号安全，请及时修改密码，谢谢！
                    """.format(name,link)

    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = "html"
    send_status = msg.send()
    EmailVerifyRecord.objects.create(code=code, email=email, send_type=send_type)
    return send_status









