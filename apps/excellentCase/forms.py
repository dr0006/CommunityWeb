# -*- coding: utf-8 -*-
"""
@File  : forms.py
@author: FxDr
@Time  : 2023/11/14 18:22
@Description:
"""
# forms.py
from django import forms
from .models import ExcellentCase


class ExcellentCaseForm(forms.ModelForm):
    class Meta:
        model = ExcellentCase
        fields = ['title', 'experience', 'category', 'village_info']
