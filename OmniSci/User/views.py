# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：views.py
#   Author：Yong Bai
#   Time：2019-04-01 20:20:39
#   Description：
#
# ================================================================

from django.views.generic.base import View
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from json import dumps
import datetime
from random import randint
from .send_email import send_email
from re import match as match
from .models import UserInfo
from .models import UnauthorizedUserInfo
from Project.models import UserProjectAuthority
from .get_info_dict import *
from .utils import FileHelper,is_pc,make_sense
import os
from os.path import exists,join
import requests


# 注册相关函数
class Register(View):
    def get(self, request):
        if is_pc(request.META['HTTP_USER_AGENT']):
            return render(request, 'User/register.html')
        else:
            return render(request, 'User/new_mobile_register.html')


    def check_info(self, post_dict):
        """
        检查用户注册的表单信息是否有效
        :param post_dict: Query_Dict from request.POST
        :return
        """
        name = post_dict.get("c_name")
        pwd1 = post_dict.get("c_pwd")
        pwd2 = post_dict.get("c_pwd2")
        email = post_dict.get("c_email")
        auth = post_dict.get("auth")
        age = post_dict.get("age")      # 年龄可以不填，但填了必须验证合法性
        # sex = post_dict.get("sex")    不验证性别
        message = post_dict.get("q_msg")
        # 可包含中文字符、数字、大写字母和小写字母，名字总长1-14字节（中文按2字节计算）
        name_pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9]{1,14}$'
        # 需包含大写字母、小写字母、标点符号和特殊字符中的至少三种，位数为8-16位
        pwd_pattern = r'^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{8,16}$'
        # 常规邮箱格式
        email_pattern = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        # 大于等于0，小于等于159岁
        age_pattern = r'^((1[0-5])|[1-9])?\d$'

        error_msg = []
        if match(name_pattern, name) == None or len(name) > 14:
            error_msg.append("Invalid name!")
        else:
            # 用户名重复
            user_info = UserInfo.objects.filter(user_name = name)
            if len(user_info) > 0:
                error_msg.append("The name had been registered!")

        if match(pwd_pattern, pwd1) == None:
            error_msg.append("Invalid password!")

        if pwd1 != pwd2:
            error_msg.append("The two passwords are different!")

        # TODO 代码风格
        if match(email_pattern, email) == None:
            error_msg.append("Invalid email address!")
        else:
            unauthorized_user_info = UnauthorizedUserInfo.objects.filter(email_address = email)
            if len(unauthorized_user_info) > 0:
                if unauthorized_user_info[0].authorization != auth:
                    error_msg.append("Authorization code is wrong!")
            else:
                error_msg.append("Please authorize your email!")
        if match(age, age_pattern) != None and age != "":
            error_msg.append("Invalid Age!")

        if len(message) > 2000:
            error_msg.append("Self introduction is too long!")

        return error_msg

    def post(self, request):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        avatar_dir = join(base_dir, 'static/images/avatar')
        post_dict = request.POST
        file_helper = FileHelper(request.FILES)

        print (post_dict)
        # 后端验证有效性
        msg = self.check_info(post_dict)

        if (len(msg) > 0):
            return render(request, 'info.html' if is_pc(request.META['HTTP_USER_AGENT']) else 'info_mobile.html', {
                'msg': msg,
                'title': u'注册失败!'
            })

        # 保存头像
        avatar_name = file_helper.write(avatar_dir)


        # 加密
        encrypted_pwd = make_password(post_dict.get("c_pwd"),"OmniSci",'pbkdf2_sha256')
        # int_age = int(post_dict.get("age")) if (post_dict.get("age") != "") else None
        int_age = int(post_dict.get("age")) if make_sense(post_dict.get("age")) else None
        sex_filter = post_dict.get("sex") if make_sense(post_dict.get("sex")) else None

        user_info = UserInfo(
            password=encrypted_pwd,
            user_name=post_dict.get("c_name"),
            user_introduction=post_dict.get("q_msg"),
            sex=sex_filter,
            age=int_age,
            email_address=post_dict.get("c_email"),
            avatar=avatar_name,
        )
        user_info.save()
        # 删除未注册的用户信息
        UnauthorizedUserInfo.objects.filter(email_address = post_dict.get("c_email")).delete()

        return render(request, 'info.html' if is_pc(request.META['HTTP_USER_AGENT']) else 'info_mobile.html', {
            'msg': [],
            'title': u'注册成功!'
        })


class SendEmail(View):

    def get_random(self):
        return randint(100000, 999999)

    def post(self, request):

        # 验证注册功能时绕过发送邮件
        debug_giggle = False

        # TODO 发验证码很慢，有用户可见延迟
        # TODO 能否优化？前端加loading界面?
        error_msg = []
        code = SendEmail.get_random(self)
        email = request.POST.get('c_email')
        name=request.POST.get('c_name')

        print (email,name)
        email_pattern = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'

        existing_email_addr = (x['email_address'] for x in UserInfo.objects.all().values('email_address'))

        if not debug_giggle:
            if not match(email_pattern, email):  # 邮箱不合法
                error_msg.append('邮箱不合法')

            elif email in existing_email_addr:
                error_msg.append('邮箱已存在')

            elif not send_email(code, name, email):
                error_msg.append('邮件发送失败')

        if (len(error_msg) == 0) or debug_giggle:
            # FIXED 该种方式是否会出错
            # 查找未验证的用户邮箱
            unauthorized_user_list = UnauthorizedUserInfo.objects.filter(email_address=email)
            if len(unauthorized_user_list) > 0: # 如果邮箱存在于未验证表中
                unauthorized_user_list[0].authorization = code
                unauthorized_user_list[0].save()
            else:
                temp_user_info = UnauthorizedUserInfo(
                    email_address = email,
                    authorization = code
                )
                temp_user_info.save()
            result = {'status':'success','code':code}
            return HttpResponse(dumps(result,ensure_ascii=False),content_type='application/json')
        else:
            result = {'status':'fail','msg':error_msg}
            return HttpResponse(dumps(result,ensure_ascii=False),content_type='application/json')


class Login(View):
    """ 用户登录页面
    """
    @staticmethod
    def get(request):
        print(request.session.get('logged_in',None))
        if is_pc(request.META['HTTP_USER_AGENT']):
            return render(request, 'User/login.html')
        else:
            return render(request, 'User/new_mobile_login.html')


    def login_validating(self,user,request):
        """
        检验密码是否正确
        :param user:
        :param request:
        :return:
        """
        password = request.POST.get('c_pwd')
        if check_password(password,user.password):
            request.session['uid'] = user.uid
            print(request.POST.get('identity'))
            request.session['user_status'] = True if request.POST.get('identity') == str(1) else False
            print(request.session.get('user_status'))
            request.session['logged_in'] = True
            return HttpResponseRedirect('/home/index')
        else:
            # 密码错误
            return render(request,'info.html' if is_pc(request.META['HTTP_USER_AGENT']) else 'info_mobile.html',{
                'msg':["密码错误"],
                'title':u'登录失败'
            })

    def post(self,request):
        """
        :param request:
        :return:
        """

        account_code = request.POST.get('c_name')
        if UserInfo.objects.filter(user_name=account_code).exists():
            user = UserInfo.objects.get(user_name=account_code)
            return self.login_validating(user,request)

        elif UserInfo.objects.filter(email_address=account_code).exists():
            user = UserInfo.objects.get(email_address=account_code)
            return self.login_validating(user,request)
        else:
            return render(request, 'info.html' if is_pc(request.META['HTTP_USER_AGENT']) else 'info_mobile.html', {
                'msg': ["用户不存在"],
                'title': u'登录失败!'
            })


class Logout(View):
    """
    响应用户注销
    """
    def get(self,request):
        """
        session标记为未登录
        :param request:
        :return:
        """

        # request.session['logged_in'] = False

        request.session.flush()

        return HttpResponseRedirect('/home/index')


class ChangeMode(View):
    """
    更改用户登录身份
    """
    def post(self,request):
        """
        志愿者与项目发布者身份转换
        :param request:
        :return:
        """

        request.session['user_status'] = not request.session.get('user_status',None)

        return HttpResponseRedirect('/home/index')

class BriefProfile(View):
    """
    导航栏获取用户信息
    """
    def post(self,request):
        data = {}
        if request.session.get('logged_in',None):
            user = UserInfo.objects.get(uid=request.session.get('uid',None))
            data['logged_in'] = True
            data['u_name'] = user.user_name
            data['avatar_path'] = user.avatar
            data['u_status'] = request.session.get('u_status',None)
            data['release'] = UserProjectAuthority.objects.filter(uid=user, authority=1).exists()
            data['volunteer'] = UserProjectAuthority.objects.filter(uid=user, authority__in=[2,3]).exists()
            data['credit'] = user.credit

        else:
            data['logged_in'] = False

        return HttpResponse(dumps(data))

class Profile(View):
    # FIXME setting.py

    def get(self,request):
        """
        如果uid和当前用户uid不一致，使用当前用户的uid
        如果当前用户未登录，跳转到登录界面
        request.session 需包括uid,user_status
        :param request:
        :return:
        """

        if(request.session.get('logged_in',None) != True):
            return Login.get(request)

        # TODO 注销一定删除session，None 改成保密
        uid = request.session.get('uid',None)
        base = get_user_info(uid)
        activity = get_user_activity(uid)
        upload_record = get_upload_data(uid)
        r_projects,a_projects,p_projects = get_user_project(uid)

        data = {}
        data['base'] = base
        data['activity'] = activity
        data['upload_record'] = dumps(upload_record)                # 在js代码中使用，因此需要先dumps成字符串 modifiede by YB
        data['release_projects'] = r_projects
        data['assist_projects'] = a_projects
        data['participate_projects'] = p_projects

        # print(data)
        if is_pc(request.META['HTTP_USER_AGENT']):
            return render(request,'User/profile.html',data)
        else:
            # return render(request, 'User/mobile_profile.html', data)
            return render(request, 'User/new_mobile_profile.html', data)


class UploadAvatar(View):
    # 用户头像裁剪页面
    def get(self,request):
        return render(request, 'User/crop.html')


class ChangePwd(View):
    """
    更改密码功能
    """
    def get(self, request):
        return render(request,'User/changePwd.html')

    def post(self,request):
        """
        原密码正确就更改密码并返回主页，否则报修改失败
        """
        post_data = request.POST

        uid = int(request.session.get('uid'))
        old_password = post_data.get('old_pwd')
        new_password = post_data.get('new_pwd')
        user = UserInfo.objects.get(uid=uid)

        if check_password(old_password,user.password):

            encrypt_password = make_password(new_password,'OmniSci','pbkdf2_sha256')
            user.password = encrypt_password
            user.save()

            return render(request, 'info.html', {
                'msg': [],
                'title': u'修改成功!'
            })

        else:
            return render(request, 'info.html', {
                'msg': ['旧密码错误'],
                'title': u'修改失败!'
            })


class DeleteAccount(View):
    def get(self,request):
        return render(request, 'User/deleteAccount.html')

    def post(self,request):
        # 如果账户删除成功的话应该顺便注销登录状态->已完成
        # 要考虑一下都删些啥，该用户发布过的项目要不要删?->不删，把项目发布者置为空

        post_data = request.POST
        uid = request.session.get('uid',None)
        user = UserInfo.objects.get(uid = uid)

        if check_password(post_data.get('pwd'),user.password):
            request.session.flush()
            user.delete()

            return render(request, 'info.html', {
                'msg': [],
                'title': u'删除成功!',
                'simple': True
            })

        else:
            return render(request, 'info.html', {
                'msg': ['密码错误'],
                'title': u'删除失败!',
                'simple': True
            })


class ChangeInfo(View):
    def get(self,request):
        if is_pc(request.META['HTTP_USER_AGENT']):
            return render(request,'User/changeInfo.html')
        else:
            return render(request,'User/mobile_changeInfo.html')

    def post(self,request):
        # TODO @ziwei
        # 修改用户信息
        # 照片储存可以参考注册过程中的相关函数，使用FileHelper
        # 前端验证邮箱格式是否合法，后端检验是否被别人注册过
        # TODO 登录判断

        base_dir = os.path.dirname(os.path.abspath(__file__))
        avatar_dir = join(base_dir, 'static/images/avatar')
        post_dict = request.POST

        user_id = request.session.get('uid',None)
        user = UserInfo.objects.get(uid = user_id)

        msg = self.check_info(user_id,post_dict)
        if len(msg) <=0:
            # 保存图片
            if request.FILES.get('image') is not None:

                file_helper = FileHelper(request.FILES)
                avatar_name = file_helper.write(avatar_dir)
                user.avatar = avatar_name

            age = post_dict.get('age')
            user.email_address = post_dict.get('email')
            user.user_introduction = post_dict.get('description')
            user.age = int(age) if age != "Secret" and age != "secret" else None
            user.sex = post_dict.get('sex') if post_dict.get('sex') != 'undefined' else None
            user.save()

            return render(request, 'info.html', {
                'msg': msg,
                'title': u'修改成功!'
            })
        else:
            return render(request, 'info.html', {
                'msg':msg,
                'title': u'修改失败!'
            })

    def check_info(self,user_id,post_dict):
        msg = []
        users = UserInfo.objects.filter(~Q(uid = user_id),email_address = post_dict.get('email'))
        if len(users)>0:
            msg.append('The email address is occupied by someone else, '
                       'please retry your operation with another email address!')

        elif len(post_dict.get('description')) > 2000:
            msg.append('The description is too long!')

        return msg

class FetchInfo(View):
    def get(self,request):
        # TODO @ziwei
        # 根据session 返回当前用户信息
        # TODO 判断用户是否登录？万一直接访问URL
        # info = {
        #     'avatar': 'images\\avatar\\353dd7ae-5e86-11e9-b17d-f1e8abb67815.png',
        #     'username': 'giggle',
        #     'description':'为了测试换行样式所以这是很长的一段话balabalbalbalabalabalabalabala',
        #     'email': 'Secret',
        #     'sex': 'Secret',
        #     'age': 'Secret'
        # }

        user_id = request.session.get('uid',None)
        user = UserInfo.objects.get(uid = user_id)

        default_introduction = u'他很懒，什么也没留下。'
        secret = 'Secret'
        info = {
            'avatar': user.avatar,
            'username': user.user_name,
            'description': user.user_introduction if len(user.user_introduction)>0 else default_introduction,
            'email': user.email_address,
            'sex': user.sex if user.sex else secret,
            'age': user.age if user.age else secret,
        }
        print('info', info)

        return HttpResponse(dumps(info),content_type="application/json")


class Debug(View):
   def get(self,request):
       return render(request, 'info.html' if is_pc(request.META['HTTP_USER_AGENT']) else 'info_mobile.html', {
           'msg': [],
           'title': u'注册成功!'
       })

########################################## debug ###########################################

def preface_debug(request):
    return render(request, 'User/mobile_preface.html')

def login_debug(request):
    return render(request, 'User/new_mobile_login.html')

def register_debug(request):
    return render(request, 'User/new_mobile_register.html')

class ProfileOri(View):
    # FIXME setting.py

    def get(self,request):
        """
        如果uid和当前用户uid不一致，使用当前用户的uid
        如果当前用户未登录，跳转到登录界面
        request.session 需包括uid,user_status
        :param request:
        :return:
        """

        if(request.session.get('logged_in',None) != True):
            return Login.get(request)

        # TODO 注销一定删除session，None 改成保密
        uid = request.session.get('uid',None)
        base = get_user_info(uid)
        activity = get_user_activity(uid)
        upload_record = get_upload_data(uid)
        r_projects,a_projects,p_projects = get_user_project(uid)

        data = {}
        data['base'] = base
        data['activity'] = activity
        data['upload_record'] = dumps(upload_record)                # 在js代码中使用，因此需要先dumps成字符串 modifiede by YB
        data['release_projects'] = r_projects
        data['assist_projects'] = a_projects
        data['participate_projects'] = p_projects

        # print(data)
        if is_pc(request.META['HTTP_USER_AGENT']):
            return render(request,'User/profile.html',data)
        else:
            return render(request, 'User/mobile_profile.html', data)
            # return render(request, 'User/new_mobile_profile.html', data)