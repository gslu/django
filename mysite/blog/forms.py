# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import Comment,Profile,PictureRecord
from django.contrib.auth.models import User

class EmailPostForm(forms.Form):
    to = forms.EmailField(label="分享至")
    comments = forms.CharField(required=False,widget=forms.Textarea,label="评语")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image",)

class BgimgForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bgimg",)

class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = PictureRecord
        fields = ("picture",)

class BasicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("nickname",'gender','motto','introduce')
        labels = {
            'nickname':'昵称',
            'gender':'性别',
            'motto': '说说',
            'introduce': '简介',
        }
        widgets = {
            "motto":forms.TextInput(attrs={'style': 'width:300px'})
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("hometown",'address','occupation','hobby')
        labels = {
            'hometown':'家乡',
            'address':'现住',
            'occupation': '职业',
            'hobby': '爱好',
        }

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone",)

class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {
            'email':'邮箱'
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    email = forms.EmailField(label=u"邮箱")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")

    #code = forms.CharField(max_length=10,label=u"序列")
    #def clean_code(self):
    #    code = self.cleaned_data['code']
    #    if code <> "l14789632":
    #        raise forms.ValidationError("注册序列错误,暂不支持注册")

    def clean_password(self):
        import re
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("密码强度须大于6")
        # 密码复杂度
        #elif not re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+',password):
        #    raise forms.ValidationError("密码至少包含字母,数字,符号其中两样")
        else:
            return password


class ForgetForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    email = forms.EmailField(label=u"邮箱")


class ResetForm(forms.Form):

    def __init__(self,*args,**kwargs):
        super(ResetForm,self).__init__(*args,**kwargs)
        #self.fields['username'].widget.attrs['readonly'] = True

    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                               max_length=40,min_length=3,label=u"帐　号")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autofocus': True}),
                               label=u"新密码",strip=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput,label=u"再一次",strip=False)

    def clean_password(self):
        import re
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("密码强度须大于6")
        #elif not re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+',password):
        #    raise forms.ValidationError("密码至少包含字母,数字,符号其中两样")
        else:
            return password

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password <> password_confirm:
            raise forms.ValidationError("前后密码不一致")
        else:
            return password_confirm


class PswdChangeForm(ResetForm):
    old_password = forms.CharField(widget=forms.PasswordInput,label="原密码",strip=False,)
    username = None

    def __init__(self,user,*args,**kwargs):
        self.user = user
        super(PswdChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码错误，请重新输入')
        return old_password



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class WriteForm(forms.Form):
    title = forms.CharField(max_length=100,label="",
                            widget=forms.TextInput(attrs={'placeholder':'文章标题'}))
    body = forms.CharField(required=False,widget=forms.Textarea,label="")


class NewBookForm(forms.Form):
    book_name = forms.CharField(max_length=14,label="",
                            widget=forms.TextInput(attrs={'placeholder':'文集名称'}))


class NewTagForm(forms.Form):
    tag_name = forms.CharField(max_length=14,label="",
                            widget=forms.TextInput(attrs={'placeholder':'标签名称'}))






