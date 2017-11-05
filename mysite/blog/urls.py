# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.views.generic.base import RedirectView

from .upload_file import uploadImage
from . import views

urlpatterns = [

    #　暂时充当网站主页
    url(r'^$',RedirectView.as_view(url='user/1/'),name="index"),

    url(r'^user/(?P<user_id>\d+)/$', views.postList, name='post_list'),
    url(r'^user/(?P<user_id>\d+)/blog/tag/(?P<tag_name>.+)/$',views.postList,name='post_list_by_tag'),

    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/(?P<id>\d+)/$',
                    views.postDetail,
                    name='post_detail'),

    url(r'^blog/(?P<post_id>\d+)/share/$',views.postShare,name='post_share'),
    url(r'^user/(?P<user_id>\d+)/music/$',views.music,name='music'),
    url(r'^user/(?P<user_id>\d+)/about/(?P<option>\w+)/$', views.about, name='about'),

    # login,logout,register
    url(r'^login/$', views.userLogin, name="user_login"),
    url(r'^logout/$', views.userLogout, name="user_logout"),
    url(r'^register/$', views.userRegister, name="user_register"),

    url(r'^verify/(?P<username>[\w\d-]+)/(?P<email>[\w\d\.@]+)/$',
                    views.verifyRegister, name='verify_register_before'),

    url(r'^verify/(?P<username>[\w\d-]+)/confirm/(?P<code>[\w\d-]+)/$', views.verifyRegister, name='verify_register_after'),
    url(r'^password/forget/$', views.pswdForget, name='pswd_forget'),
    url(r'^password/reset/(?P<username>[\w\d-]+)/(?P<code>[\w\d-]+)/$', views.pswdReset, name='pswd_reset'),

    url(r'^blog/manage/$', views.postManage, name='post_manage'),
    url(r'^blog/write/$', views.writePost, name='write_post'),
    url(r'^blog/edit/(?P<post_id>\d+)/$', views.editPost, name='edit_post'),
    url(r'^blog/edit/(?P<post_id>\d+)/(?P<opt>\w+)/$', views.editPost, name='publish'),
    url(r'^upload/$', uploadImage, name='upload_image'),
]