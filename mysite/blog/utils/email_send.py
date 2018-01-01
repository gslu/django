#coding:utf-8

from django.core.mail import EmailMessage
from django.conf import settings
from django.core.urlresolvers import reverse
from ..models import VerifyRecord
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import uuid



def sendEmail(subject, message, email_from, to):
    HOST = settings.EMAIL_HOST
    msg=MIMEText(message,'html',"utf-8")
    msg['Subject'] = subject

    h = Header('浮文掠影', 'utf-8')
    h.append('<{}>'.format(email_from), 'ascii')

    msg['From'] = h
    msg['To'] = ",".join(to)

    server = smtplib.SMTP_SSL()
    server.connect(HOST,465)
    server.login(email_from, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(email_from,to,msg.as_string())
    server.quit()
    return True




def sendVerifyEmail(email, name, send_type="register", request=None):
    #code = ''.join(random.sample('0123456789', 5))
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

    #msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    #msg.content_subtype = "html"
    #send_status = msg.send()
    ret = sendEmail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    VerifyRecord.objects.create(code=code, email=email, send_type=send_type)
    return ret









