# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.views.generic.base import RedirectView

from .upload_file import uploadImage,addImage,addBgimg
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
    url(r'^user/(?P<user_id>\d+)/picture/$', views.picture, name='picture'),
    url(r'^user/(?P<user_id>\d+)/about/(?P<option>\w+)/$', views.about, name='about'),

    # 登录　注册　退出
    url(r'^login/$', views.userLogin, name="user_login"),
    url(r'^logout/$', views.userLogout, name="user_logout"),
    url(r'^register/$', views.userRegister, name="user_register"),

    # 注册验证，忘记密码
    url(r'^verify/(?P<username>[\w\d-]+)/(?P<email>.+)/$',
                    views.verifyRegister, name='verify_register_before'),
    url(r'^verify/(?P<username>[\w\d-]+)/confirm/(?P<code>[\w\d-]+)/$', views.verifyRegister, name='verify_register_after'),
    url(r'^password/forget/$', views.pswdForget, name='pswd_forget'),
    url(r'^password/reset/(?P<username>[\w\d-]+)/(?P<code>[\w\d-]+)/$', views.pswdReset, name='pswd_reset'),

    #　文章管理
    url(r'^blog/manage/$', views.postManage, name='post_manage'),
    url(r'^blog/manage/books/(?P<book_id>\d+)/$', views.postManage, name='select_book'),
    url(r'^blog/manage/books/(?P<book_id>\d+)/tags/(?P<tag_name>.+)/$', views.postManage, name='select_tag'),

    #　文章新建,编辑
    url(r'^blog/write/books/(?P<book_id>\d+)/tags/(?P<tag_name>.+)/$', views.writePost, name='write_post'),
    url(r'^blog/edit/(?P<post_id>\d+)/$', views.editPost, name='edit_post'),

    # 文章保存，发布　ajax异步调用接口
    url(r'^blog/edit/(?P<post_id>\d+)/(?P<opt>\w+)/$', views.editPost, name='publish'),

    # 个人中心
    url(r'^center/$', views.center, name='center'),

    # 富文本图片上传处理接口
    url(r'^upload/$', uploadImage, name='upload_image'),

    # 个人中心头像变更
    url(r'^upload/image/$', addImage, name='upload_u_image'),

    # 个人中心背景变更
    url(r'^upload/bgimg/$', addBgimg, name='upload_bgimg'),

    # 个人中心设置保存
    url(r'^center/save/$', views.settingSave, name='setting_save'),

    # 文章管理
    url(r'^book/rename/$', views.bookReName, name='book_rename'),
    url(r'^tag/rename/$', views.tagReName, name='tag_rename'),
    url(r'^book/delete/$', views.delBook, name='book_delete'),
    url(r'^tag/delete/$', views.delTag, name='tag_delete'),
    url(r'^post/delete/$', views.delPost, name='post_delete'),
    url(r'^post/change_tag/$', views.changeTag, name='change_tag'),
    url(r'^tag/change_book/$', views.changeBook, name='change_book'),

    # 关注
    url(r'^user/(?P<user_id>\d+)/edit_follow/$', views.editFollow, name='edit_follow'),
]