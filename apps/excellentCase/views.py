# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render, redirect

from .forms import ExcellentCaseForm
from .models import ExcellentCase


# 案例清单页面展示
def case_list(request):
    cases = ExcellentCase.objects.all()
    return render(request, './excellentCase/case_list.html', {'cases': cases})


# 发布优秀案例
@login_required
def publish_case(request, category):
    if request.method == 'POST':
        form = ExcellentCaseForm(request.POST)
        if form.is_valid():
            excellent_case = form.save()
            # 处理发布成功后的逻辑
            return redirect('case_list')  # 重定向到案例列表页面
    else:
        initial_data = {'category': category}  # 设置默认分类
        form = ExcellentCaseForm(initial=initial_data)

    return render(request, './excellentCase/publish_case.html', {'form': form})


def case_detail(request, case_id):
    """案例详情"""
    case = get_object_or_404(ExcellentCase, id=case_id)
    return render(request, './excellentCase/case_detail.html', {'case': case})


def filter_cases(request):
    """案例筛选路由"""
    # 获取筛选条件
    province = request.GET.get('province', '')  # 省份
    terrain_type = request.GET.get('terrain_type', '')  # 地形类型
    industry_type = request.GET.get('industry_type', '')  # 主要产业类型
    village_size = request.GET.get('village_size', '')  # 村庄规模
    min_avg_income = request.GET.get('min_avg_income', '')  # 最低年平均收入

    # 筛选条件的字典
    filters = {}
    if province:
        filters['village_info__province'] = province
    if terrain_type:
        filters['village_info__terrain'] = terrain_type
    if industry_type:
        # 使用__contains进行模糊匹配
        filters['village_info__industry__contains'] = industry_type
    if village_size:
        filters['village_info__village_size'] = village_size
    if min_avg_income:
        filters['village_info__avg_income__gte'] = min_avg_income

    # 获取符合条件的案例列表
    cases = ExcellentCase.objects.filter(**filters)
    print(cases)

    return render(request, 'excellentCase/filtered_cases.html', {'cases': cases})


def search_excellent_case(request):
    query = request.GET.get('q')
    results = ExcellentCase.objects.filter(
        Q(title__icontains=query) | Q(experience__icontains=query) | Q(category__icontains=query)
    )
    context = {'query': query, 'results': results}
    return render(request, 'excellentCase/search_case_results.html', context)
