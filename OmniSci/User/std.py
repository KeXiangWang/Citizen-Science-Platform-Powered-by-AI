# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：std.py
#   Author：Yong Bai
#   Time：2019-04-05 19:49:05
#   Description：定义数据展示界面的数据字段
#
# ================================================================

import datetime

data = {
    'type': 'volunteer/promulgator',
    # 用户的登录身份，志愿者还是发布者
    'base': {
        # 基础信息
        'avatar': 'images/avatar.png',
        # 头像url
        'name': 'byby221b',
        # 用户名
        'description': 'my name is ...',
        # 用户自我介绍，没有的话用缺省的描述
        'email': 'hellobaiyong@163.com',
        # 邮箱
        'sex': 'male or female or null',
        # 性别，分三种，男、女和保密
        'age': '21',
        # 年龄
        'star': '50'
        # 信誉
    },
    'activity':
    # 最近的十条活动记录
        [
            {
                'date': '2019-04-05',
                # 活动日期
                'type': 'upload/join/assist/release',
                # 活动类型，志愿者可能提交数据、参与项目、审核数据，发布者可能发布项目、审核数据
                'project': 'p1'
                # 所涉及的项目名称
            },
            {
                'date': '2019-04-03',
                'type': 'upload/join/assist/release',
                'project': 'p1'
            }
        ]
    ,
    'upload_record': {  # def get_user_data(user_id)
        # 用户上传数据数量统计（只针对志愿者），键为日期，键值为当日上传的数据量
        '2019-04-03': 32,
        '2019-04-02': 12,
        '2019-04-01': 0,
    },
    'participate_projects': [
        # 用户参与的所有项目（假如身份是志愿者）或发布的所有项目(假如身份是发布者)
        {
            'name': 'p1',
            # 项目名
            'date': datetime.datetime(2019,4,22),
            # 项目发布日期
            'desc': 'The project is for ...',
            # 项目描述
            'area': 'animal',
            # 项目所属领域
            'cover': '/static/project_image/Crape myrtle_0.jpg',
            # 项目封面图
            'id':23
        }
    ],
    'assist_projects':[
        {
            'name': 'p2',
            'date': datetime.datetime(2019,4,22),
            'desc': 'The project is for ...',
            'area': 'animal',
            'id':12,
            'cover': '/static/project_image/Crape myrtle_0.jpg'
        }
    ],
    'release_projects':[
        {
            'name': 'p3',
            'date': datetime.datetime(2019,4,22),
            'desc': 'The project is for ...',
            'area': 'animal',
            'id':42,
            'cover': '/static/project_image/Crape myrtle_0.jpg'
        }
    ]
}
