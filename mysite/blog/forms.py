# -*- coding: utf-8 -*-
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    to = forms.EmailField(label="分享至")
    comments = forms.CharField(required=False,widget=forms.Textarea,label="评语")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    email = forms.EmailField(label=u"邮箱")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")


class ForgetForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    email = forms.EmailField(label=u"邮箱")




