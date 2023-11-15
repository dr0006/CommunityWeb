from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import User, TopicComment, Topic

# 注册管理后台 表
admin.site.register(User)
admin.site.register(TopicComment)
admin.site.register(Topic)
