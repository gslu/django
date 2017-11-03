# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import Comment

class EmailPostForm(forms.Form):
    to = forms.EmailField(label="分享至")
    comments = forms.CharField(required=False,widget=forms.Textarea,label="评语")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)



class LoginForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    email = forms.EmailField(label=u"邮箱")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")
    code = forms.CharField(max_length=10,label=u"序列")
    def clean_password(self):
        import re
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("密码强度须大于6")
        elif not re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+',password):
            raise forms.ValidationError("密码至少包含字母,数字,符号其中两样")
        else:
            return password


class ForgetForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    email = forms.EmailField(label=u"邮箱")


class ResetForm(forms.Form):

    def __init__(self,*args,**kwargs):
        super(ResetForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")
    password_confirm = forms.CharField(widget=forms.PasswordInput,label=u"确认")

    def clean_password(self):
        import re
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("密码强度须大于6")
        elif not re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+',password):
            raise forms.ValidationError("密码至少包含字母,数字,符号其中两样")
        else:
            return password

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password <> password_confirm:
            raise forms.ValidationError("前后密码不一致")
        else:
            return password_confirm


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class WriteForm(forms.Form):
    title = forms.CharField(max_length=100,label="",
                            widget=forms.TextInput(attrs={'placeholder':'文章标题'}))
    body = forms.CharField(required=False,widget=forms.Textarea,label="")



