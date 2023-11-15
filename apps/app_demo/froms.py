# -*- coding: utf-8 -*-
"""
@File  : froms.py
@author: FxDr
@Time  : 2023/10/28 18:46
@Description:
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.app_demo.models import User, Topic, TopicComment, PrivateMessage


# 注册
class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


# 个人资料
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'remarks', 'Gender_user', 'User_Type', 'last_name', 'first_name', 'image']


# 帖子
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'desc_topic', 'category']


# 评论
class CommentForm(forms.ModelForm):
    class Meta:
        model = TopicComment
        fields = ['body']


# 私信
class MessageSendForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']
