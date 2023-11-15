# -*- coding: utf-8 -*-
"""
@File  : urls.py
@author: FxDr
@Time  : 2023/11/14 18:32
@Description:
"""
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('publish_case/<str:category>/', views.publish_case, name='publish_case'),
    path('case_list/', views.case_list, name='case_list'),  # 案例列表清单
    path('case_detail/<int:case_id>/', views.case_detail, name='case_detail'),  # 案例的详情页面
    path('filter_cases/', views.filter_cases, name='filter_cases'),  # 筛选案例
    path('search_case/', views.search_excellent_case, name='search_case'),  # 模糊搜索案例
]
