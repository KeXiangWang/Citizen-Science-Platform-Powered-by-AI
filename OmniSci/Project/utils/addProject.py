# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：addProject.py
#   Author：Yong Bai
#   Time：2019-04-09 22:38:39
#   Description： move utils.py to addProject.py
#
# ================================================================


from Project.models import DomainInfo as DM
from Project.models import ProjectInfo as PM
from Project.models import IssueInfo as IM
from Project.models import UserProjectAuthority
from User.models import UserInfo
from Project.models import ProjectIssue
from Project.models import ProjectImage
from Project.models import DataInfo
from Project.models import CommentInfo as CM
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime, timedelta
from random import randint
import json as js
import os
from os.path import exists, join


# 用于批量添加项目(但是感觉项目描述有点简陋)
def addProjects():
    print(os.getcwd())
    with open('Project/utils/data.json', 'r') as f:
        data = js.load(f)

    # print (data)
    # return
    # domains = ['动物','水果','航空','植物','医学']
    for dm in DM.objects.all():
        dm.delete()
    for idx, domain_name in enumerate(data.keys()):
        DM.objects.create(aid=idx, domain_name=domain_name)

    print('result', DM.objects.all())

    pid = 0
    for project in PM.objects.all():
        project.delete()
    for domainName, items in data.items():
        domain = DM.objects.filter(domain_name=domainName).first()
        for chName, enName in items.items():
            pid += 1
            keyword = enName.lstrip('The ').lstrip("A ")
            imgName = 'default.png'
            root = 'Project/static/project_image'
            for i in range(3):
                if exists(join(root, '{}_{}.jpg'.format(keyword, i))):
                    imgName = '{}_{}.jpg'.format(keyword, i)
                    break
            PM(
                projection_name=chName,
                projection_introduction='{}_{}\t{}'.format(domainName, chName, enName),
                area=domain,
                projection_image='{}{}'.format('/static/project_image/', imgName),
                publish_time=timezone.now() - timedelta(days=randint(50, 150)),
            ).save()
    print("Successfully Add Projects")


def addIssue():
    import random
    import string
    project = PM.objects.filter(pid=1)[0]
    for i in range(55):
        IM(
            title='title_{}'.format(i),
            description='ABCDE12345'
        ).save()

        new_issue = IM.objects.last()

        ProjectIssue(
            pid=project,
            issue_id=new_issue
        ).save()

        for j in range(55):
            CM(
                issue_id=new_issue,
                text=''.join(random.sample(string.ascii_letters + string.digits, 16))
            ).save()


def addImage():
    name_list = ['wangkexiang', 'baiyong', 'xiafeiyu', 'qinziwei', 'xuxiangrong', 'renhouxing']
    path = "Project/static/project_data/"
    data_path_prefix = '/static/project_data/'
    image_set = [x for x in os.listdir(path)]
    for i in range(1, 9):
        time_stamp = timezone.now() - timedelta(50)
        project = PM.objects.filter(pid=i)[0]
        if i < 7:
            user = UserInfo.objects.filter(user_name=name_list[i - 1])[0]
        else:
            user = UserInfo.objects.filter(uid=i)[0]
        if UserProjectAuthority.objects.filter(pid=i, uid=i) == []:
            # print("fuck--------------")
            UserProjectAuthority(
                pid=project,
                uid=user,
                authority=3,
                register_time=time_stamp,
            ).save()
        for j in range(1, 21):
            count = (i - 1) * 20 + j
            id = 'data_' + str(count) + '.'
            id_len = len(id)
            data_name = [x for x in image_set if x[0:id_len] == id][0]
            # print(data_name, count)
            data_path = data_path_prefix + data_name
            verified = 0 if j < 12 else 1
            DataInfo(
                data_type='image',
                data_name=project.projection_name + str(j),
                data_path=data_path,
                data_time=time_stamp + timedelta(days=randint(2, 50)),
                data_location="北京市",
                data_province="北京" if j < 10 else "山西" if j < 15 else "广东",
                uid=user,
            ).save()
            ProjectImage(
                pid=project,
                data_id=DataInfo.objects.last(),
                verified=verified,
            ).save()
    print("Successfully Add Images")


def addUser():
    name_list = ['wangkexiang', 'baiyong', 'xiafeiyu', 'qinziwei', 'xuxiangrong', 'renhouxing']
    password_list = ['WangKX1606', 'BaiY1606', 'XiaFY1606', 'QinZW1606', 'XuXR1606', 'RenHX1606']
    for i in range(30):
        if i < 6:
            name = name_list[i]
            password = make_password(password_list[i], "OmniSci", 'pbkdf2_sha256')
            user_introduction = "OmniSci创始人"
            sex = True
            age = 21
            email_address = name + "@buaa.edu.cn"
            avatar = '/static/project_panel/cat.jpg'
        else:
            name = "User{}".format(i)
            password = make_password(name + '1606', "OmniSci", 'pbkdf2_sha256')
            user_introduction = "OmniSci僵尸用户"
            sex = False
            age = 99
            email_address = name + "@bhu.edu.cn"
            avatar = '/static/project_panel/cat.jpg'
        user_info = UserInfo(
            password=password,
            user_name=name,
            user_introduction=user_introduction,
            sex=sex,
            age=age,
            email_address=email_address,
            avatar=avatar,
        )
        user_info.save()
    print("Successfully Add Users")


def addUserProjectAuthority():
    name_list = ['wangkexiang', 'baiyong', 'xiafeiyu', 'qinziwei', 'xuxiangrong', 'renhouxing']
    number = 3
    for i in range(1, 7):
        user = UserInfo.objects.filter(user_name=name_list[i - 1])[0]
        for j in range(number):
            pid = (i - 1) * number + j + 1
            # print(pid)
            project = PM.objects.filter(pid=pid)[0]
            PM.objects.filter(pid=pid).update(publisher=user)
            UPA = UserProjectAuthority(
                uid=user,
                pid=project,
                authority=1,
            )
            UPA.save()
    print("Successfully Add Publisher For Projects")
