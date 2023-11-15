# -*- coding: utf-8 -*-
"""
@File  : urls.py
@author: FxDr
@Time  : 2023/10/29 11:36
@Description:
"""
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import CustomPasswordChangeDoneView

urlpatterns = [
    path("", views.community, name="community"),
    # path('', views.hello),

    # login,logout,register,change password,password reset by email
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="user_logout"),

    path('main_page', views.main_page, name="main_page"),
    path('index/', views.index, name='index'),
    path('Community/', views.community, name="community"),

    path('about/', views.about_us, name="about"),
    path('register/', views.user_register, name="register"),
    path('user_info/', views.user_info, name="user_info"),

    # 编辑个人资料
    path('edit_profile', views.edit_profile, name="edit_profile"),

    # 密码更改表单
    path('pwdc/', auth_views.PasswordChangeView.as_view(
        template_name='password/password_change_form.html'), name='password_change'),

    # 密码更改完成页面
    path('pwdd/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    # 需要配置邮件发送服务器
    # 密码重置表单
    path('reset_form/', auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'),
         name='password_reset'),

    # 密码重置完成页面
    path('reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),

    # 密码重置确认页面
    path('reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # 密码重置完成页面
    path('reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),

    # forum
    path('forum/', views.forum, name='forum'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('add_topic', views.add_topic, name='add_topic'),
    path('hot_topic', views.hot_topic, name='hot_topic'),
    path('my_topic', views.my_topic, name='my_topic'),
    path('search/', views.search_results, name='search_results'),

    # message
    path('inbox/', views.inbox, name='inbox'),
    # 分类筛选路由
    path('category/<int:category_id>/', views.category_view, name='category'),
]
