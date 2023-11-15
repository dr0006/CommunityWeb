# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
# 村庄的基本信息
class VillageInfo(models.Model):
    village_name = models.CharField(max_length=100, verbose_name="村庄名称", default='Unknown')
    province = models.CharField(max_length=50, verbose_name="所在省份")
    population = models.PositiveIntegerField(verbose_name="人口体量")
    resources = models.TextField(verbose_name="资源禀赋")
    industry = models.CharField(max_length=50, verbose_name="主要产业")
    terrain = models.CharField(max_length=50, verbose_name="地形")
    village_size = models.CharField(max_length=50, verbose_name="村庄规模")
    avg_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="年平均收入")

    def __str__(self):
        return f"{self.province} - {self.village_name}"


# 优秀案例
class ExcellentCase(models.Model):
    CATEGORY_CHOICES = [
        ('industrial', '产业振兴'),
        ('talent', '人才振兴'),
        ('cultural', '文化振兴'),
        ('ecological', '生态振兴'),
        ('organizational', '组织振兴'),
    ]

    DEFAULT_CATEGORY = 'industrial'

    title = models.CharField(max_length=100, verbose_name="案例标题")
    experience = models.TextField(verbose_name="经验描述")
    # 默认分类为产业振兴
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY,
                                verbose_name="案例分类")
    description = models.CharField(max_length=150, verbose_name="案例简短说明", default='我是优秀案例的简短说明。')
    village_info = models.ForeignKey(VillageInfo, on_delete=models.CASCADE, verbose_name="关联村庄信息")

    def __str__(self):
        return self.title
