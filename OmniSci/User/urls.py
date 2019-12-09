"""OmniSci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    # 界面类

    path(r'register/', views.Register.as_view(), name='register'),
    # 注册页面
    path(r'login/', views.Login.as_view(), name='login'),
    # 登录页面
    path(r'profile/', views.Profile.as_view(), name='profile'),
    # 用户信息展示界面
    path(r'avatar/',views.UploadAvatar.as_view(), name='avatar'),
    # 头像上传界面,layer
    path(r'change-pwd/', views.ChangePwd.as_view(), name='change_pwd'),
    # 密码修改界面,layer
    path(r'delete-account/', views.DeleteAccount.as_view(), name='delete_account'),
    # 删除账户界面
    path(r'change-info/', views.ChangeInfo.as_view(), name='change_info'),
    # 修改个人信息界面
    path(r'debug/', views.Debug.as_view(), name='showTemp'),
    # 用来debug的随便展示什么界面


    # 请求类

    path(r'logout/',views.Logout.as_view(),name='logout'),
    # 注销登录
    path(r'send/', views.SendEmail.as_view(), name='send_mail'),
    # 发送邮件的请求
    path(r'change-mode/', views.ChangeMode.as_view(),name='change_mode'),
    # 修改账户身份
    path(r'userinfo/', views.FetchInfo.as_view(),name='fetch_info'),
    # 导航栏用户信息获取
    path(r'brief-profile/',views.BriefProfile.as_view(), name='brief_profile'),



    # debug
    path(r'profile/debug/', views.ProfileOri.as_view() , name='profile_debug'),
    path(r'preface/debug', views.preface_debug , name='preface_debug'),
    path(r'login/debug', views.login_debug, name='login_debug'),
    path(r'register/debug', views.register_debug, name='register_debug')
]
