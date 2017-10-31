# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

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

    #class Media:
        #css = ("blog/simditor/styles/simditor.css",)
        #js = ("blog/simditor/scripts/jquery.min.js",
        #      "blog/simditor/scripts/module.js",
        #      "blog/simditor/scripts/hotkeys.js",
        #      "blog/simditor/scripts/uploader.js",
        #      "blog/simditor/scripts/simditor.js",
        #      "blog/simditor/init.js",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'post', 'body')

class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ("__unicode__","send_time")
    list_filter = ("send_time",)


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(AccessRecord,AccessRecordAdmin)
admin.site.register(MessageRecord,MessageRecordAdmin)

admin.site.register([PostClass])



