# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('name','user','created')

class AccessRecordAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','access_time')


class MessageRecordAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'send_time')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nickname',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    ordering = ['status', 'publish']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)

    class Media:
        js = ("blog/simditor/scripts/jquery.min.js",
              "blog/simditor/scripts/module.js",
              "blog/simditor/scripts/hotkeys.js",
              "blog/simditor/scripts/uploader.js",
              "blog/simditor/scripts/simditor.js",
              "blog/simditor/scripts/init.js",)

class PostClassAdmin(admin.ModelAdmin):
    list_display = ("post","post_type")
    search_fields = ("post",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'post', 'body')

class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ("__unicode__","send_time")
    list_filter = ("send_time",)

class PictureRecordAdmin(admin.ModelAdmin):
    list_display = ("user","picture","created")
    list_filter = ("user",)

class UserRelationAdmin(admin.ModelAdmin):
    list_display = ("user","follower","follow_time")

class CollectionAdmin(admin.ModelAdmin):
    list_display = ("user","collect_post","collect_time")

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(VerifyRecord,EmailVerifyRecordAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(AccessRecord,AccessRecordAdmin)
admin.site.register(MessageRecord,MessageRecordAdmin)
admin.site.register(PostClass,PostClassAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(PictureRecord,PictureRecordAdmin)
admin.site.register(UserRelation,UserRelationAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(Pv)



