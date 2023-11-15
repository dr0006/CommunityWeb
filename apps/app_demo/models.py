# -*- coding: utf-8 -*-
from ckeditor.fields import RichTextFormField
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.utils import timezone


# 用户
class User(AbstractUser):
    """User model"""
    USER_TYPE_CHOICES = [
        ('villager', '村庄'),
        ('young_adult', '年轻人'),
        ('college_student', '大学生'),
        ('research_team', '科研团队'),
        ('business', '企业'),
    ]

    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    UserID = models.AutoField(primary_key=True)
    remarks = models.CharField(max_length=500, null=True, blank=True, default="该用户暂未设置签名")
    # Email = models.CharField(max_length=255, unique=True)
    User_Type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    Gender_user = models.CharField(max_length=20, choices=GENDER_CHOICES)

    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100,
                              verbose_name="用户头像")

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.User_Type
        return self.username  # 给评论作者为用户名


class Category(models.Model):
    """ 博客的分类模型 """
    name = models.CharField(max_length=32, verbose_name="分类名称")
    desc_category = models.TextField(max_length=200, blank=True, default='', verbose_name="分类描述")

    class Meta:
        verbose_name = "帖子分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 论坛
class Topic(models.Model):
    """博客的话题模型"""
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name="标题")
    desc_topic = models.TextField(blank=True, default='', verbose_name="文章描述")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    # content = models.TextField(max_length=20000, blank=True, default='', verbose_name="内容")
    content = models.TextField(max_length=20000, blank=True, default='', verbose_name="内容")
    # 创建时间，默认为当前时间
    time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    # 作者，与 'User' 模型关联 就是外键
    author = models.ForeignKey('User', related_name='topic_author', on_delete=models.CASCADE, null=True,
                               blank=True, verbose_name="作者")
    # 评论数量，默认为0
    remarks = models.PositiveIntegerField(default=0, verbose_name="评论数量")
    # 浏览次数，默认为0
    views = models.PositiveIntegerField(default=0, verbose_name="浏览数量")

    class Meta:
        verbose_name = "论坛帖子"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 返回主题的内容作为字符串表示
        return self.content

    def increase_remarks(self):
        # 增加评论数量
        self.remarks += 1
        self.save(update_fields=['remarks'])

    def increase_views(self):
        # 增加浏览次数
        self.views += 1
        self.save(update_fields=['views'])


# from ckeditor.fields import RichTextField
# 需要上传图片功能
from ckeditor_uploader.fields import RichTextUploadingField


class TopicComment(models.Model):
    """帖子评论的模型"""
    # 外键关联到主题（Topic），当主题被删除时，相关的评论也会被删除
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, null=True, blank=True)

    # 外键关联到自身，用于表示评论的回复关系，当评论被删除时，相关的回复也会被删除
    comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    body = models.TextField(max_length=20000, blank=True, default='', verbose_name="内容")

    # 评论时间，默认为当前时间
    time = models.DateTimeField(default=timezone.now)

    # 外键关联到用户，表示评论的作者，当用户被删除时，相关的评论也会被删除
    author = models.ForeignKey('User', related_name='TopicComment_Author', on_delete=models.CASCADE, null=True,
                               blank=True)

    class Meta:
        verbose_name = "帖子评论"
        verbose_name_plural = verbose_name
        ordering = ('time',)

    def __str__(self):
        return self.body[:20]


class PrivateMessage(models.Model):
    """私信模型"""
    sender = models.ForeignKey('User', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('User', related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()  # TextField 存储更长
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # 布尔表示消息是否已读

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']  # 根据时间戳倒序排序私信
        verbose_name = "私信"
        verbose_name_plural = verbose_name
