# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

from apps.app_demo.froms import RegistrationForm, UserInfoForm, TopicForm, CommentForm, MessageSendForm
from apps.app_demo.models import User, Topic, TopicComment, PrivateMessage

"""
 django.http模块中定义了HttpResponse 对象的API
 作用：不需要调用模板直接返回数据
 HttpResponse属性：
    content: 返回内容,字符串类型
    charset: 响应的编码字符集
    status_code: HTTP响应的状态码
"""

"""
request 请求
response 相应
hello为视图函数，每个视图函数必须第一个参数为request。
request是django.http.HttpRequest的一个实例
"""


# hello world
def hello(request):
    return HttpResponse('Hello World')


# 引导页
# def index(request):
#     return render(request, "index.html")
def index(request):
    return render(request, "index-2.html")


# 登录
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "Community.html")
        else:
            # 返回登录错误信息
            context = {'login_err': 'Username or Password is wrong!'}
            return render(request, "login.html", context)
    return render(request, "login.html", {})


# 登出
@login_required
def user_logout(request):
    logout(request)
    # return HttpResponseRedirect("/topic/index")
    return redirect("main_page")


# 注册
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form.is_valid())
        # print(form.errors)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # 保存其他用户信息
            # .....

            # 让用户保持登录状态
            user = authenticate(username=username, password=password)
            login(request, user)

            # 重定向到登录成功后的页面或其他页面
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


# 个人资料
@login_required
def user_info(request):
    return render(request, 'profile/user_profile.html')


# 关于我们
def about_us(request):
    return render(request, "about.html")


# 登录后的主页
# @login_required
def community(request):
    return render(request, "Community.html")


# 编辑个人资料
@login_required
def edit_profile(request):
    user = User.objects.get(pk=request.user.pk)
    user_info_form = UserInfoForm(request.POST, request.FILES, instance=request.user)
    if user_info_form.is_valid():
        user_info_form.save()
        return HttpResponseRedirect("/users/user_info")
    else:
        user_info_form = UserInfoForm(instance=user)
    return render(request, 'profile/edit_profile.html', context={'user_info_form': user_info_form})


# 修改完密码之后重新登陆
class CustomPasswordChangeDoneView(LoginView):
    template_name = 'password/password_change_done.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            # 用户已经登录，执行注销操作
            from django.contrib.auth import logout
            logout(request)
        return response

    def get_redirect_url(self):
        # 重定向到登录页面
        return '/topic/login'


# 显示主页的贴子数，分页显示
def forum(request):
    # 获取所有主题，并按时间降序排序，以便显示最新的主题
    latest_topic_list = Topic.objects.order_by('-time')

    # 创建一个分页器，每页显示5个主题
    paginator = Paginator(latest_topic_list, 5)

    # 获取URL参数中的当前页数
    page = request.GET.get('page')

    try:
        # 获取指定页的主题列表
        latest_topic = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面号不是整数，交付第一页。
        latest_topic = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围（例如9999），则交付最后一页的结果。
        latest_topic = paginator.page(paginator.num_pages)

    # 将主题列表传递到模板中
    context = {'latest_topic': latest_topic}

    # 渲染 forum.html 模板，并传递主题列表给模板
    return render(request, 'forum/forum.html', context)


# 增加帖子
@login_required
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            # 预处理数据，添加作者信息
            _ = form.save(commit=False)
            _.author = request.user  # 假设你的主题模型有一个名为"author"的外键字段
            _.save()
            return redirect('forum')  # 使用URL名称 "forum"
    else:
        form = TopicForm()
    return render(request, 'forum/add_topic.html', {'form': form})


# topic
@login_required
def topic(request, topic_id):
    try:
        _ = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        raise Http404("不存在不存在")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 获取当前登录用户
            user = request.user
            clean_data = form.cleaned_data
            clean_data['topic'] = _
            clean_data['author'] = user  # 设置评论的作者
            TopicComment.objects.create(**clean_data)
            # 重置表单
            form = CommentForm()
            # 增加主题的评论数量
            _.increase_remarks()

    else:
        form = CommentForm()

    context = {
        'topic': _,
        'form': form
    }

    return render(request, 'forum/topic.html', context)


# 热门帖子
def hot_topic(request):
    # 获取所有主题，按评论数量降序排列
    latest_topic_list = Topic.objects.order_by('-remarks')

    # 创建分页器，每页显示5个主题
    paginator = Paginator(latest_topic_list, 5)

    # 获取当前页数（从请求中获取）
    page = request.GET.get('page')

    try:
        # 获取指定页的主题列表
        latest_topic = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整数，返回第一页
        latest_topic = paginator.page(1)
    except EmptyPage:
        # 如果页数超出范围，返回最后一页
        latest_topic = paginator.page(paginator.num_pages)

    # 构建上下文，包含分页后的主题列表
    context = {'latest_topic': latest_topic}

    # 渲染热门主题页面，传递上下文数据
    return render(request, 'forum/hot_topic.html', context)


# “我”的发布帖子
def my_topic(request):
    # 查询特定用户发布的帖子，这里假设使用用户的 ID 进行查询
    user_topics = Topic.objects.filter(author=request.user)

    context = {'user_topics': user_topics}

    return render(request, 'forum/user_topics.html', context)


# 私信收件箱
@login_required
def inbox(request):
    # 获取当前已登录用户
    global message_list
    user = request.user

    # 处理消息排序和消息发送
    if request.method == 'POST':
        if 'messageSortByDate' in request.POST:
            message_list = PrivateMessage.objects.filter(Q(receiver=user)).order_by('-timestamp')
        elif 'messageSortByUnread' in request.POST:
            message_list = PrivateMessage.objects.filter(Q(receiver=user, is_read=False)).order_by('-timestamp')
        elif 'messageSortByFT' in request.POST:
            message_list = PrivateMessage.objects.filter(Q(receiver=user)).order_by('sender__username')
        elif 'messageSend' in request.POST:
            form = MessageSendForm(request.POST)
            if form.is_valid():
                try:
                    receiver = User.objects.get(username=request.POST['receiver'])
                    message = PrivateMessage(sender=user, receiver=receiver, content=request.POST['content'])
                    message.save()
                except User.DoesNotExist:
                    print('找不到此用户')
            message_list = PrivateMessage.objects.filter(Q(receiver=user)).order_by('-timestamp')
    else:
        message_list = PrivateMessage.objects.filter(Q(receiver=user)).order_by('-timestamp')

    # 创建对话列表
    conversation = []
    contacts = set()
    for message in message_list:
        # 确定与用户交互的联系人
        contact = message.sender if message.receiver == user else message.receiver
        if contact not in contacts:
            conversation.append(message)
            contacts.add(contact)

    # 分页显示
    paginator = Paginator(conversation, 5)
    page = request.GET.get('page', 1)
    try:
        latest_conversation = paginator.page(page)
    except PageNotAnInteger:
        latest_conversation = paginator.page(1)
    except EmptyPage:
        latest_conversation = paginator.page(paginator.num_pages)

    context = {'latest_conversation': latest_conversation}

    return render(request, 'message/inbox.html', context)


def category_view(request, category_id):
    """根据分类展示求助帖"""
    # 根据 category_id 过滤相应的帖子
    topics = Topic.objects.filter(category_id=category_id)

    return render(request, 'forum/category_topic.html', {'topics': topics})


def main_page(request):
    # 获取所有主题，按评论数量降序排列
    hot_topics = Topic.objects.order_by('-remarks')[:5]  # 只获取前五个热门主题

    # 构建上下文，包含热门主题数据
    context = {'hot_topics': hot_topics}

    # 渲染主页，传递上下文数据
    return render(request, 'main_page.html', context)


# 搜索框模糊搜索
def search_results(request):
    query = request.GET.get('q', '')
    results = Topic.objects.filter(title__icontains=query) | Topic.objects.filter(content__icontains=query)
    context = {'results': results, 'query': query}
    return render(request, 'forum/search_results.html', context)
