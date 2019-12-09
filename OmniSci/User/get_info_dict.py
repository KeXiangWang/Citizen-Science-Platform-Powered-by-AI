# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：get_info_dict.py
#   Author：Xiangrong Xu
#   Time：2019/4/4 23:16
#   No Bug
#   这个文件包含所有查询用户信息的方法
# ================================================================

from User.models import *
from Project.models import *
from django.db import connection
import pytz
from datetime import datetime

def get_user_info(user_id):  # 传入用户id,返回该id的用户信息
    std_user_info = {}
    user_info = UserInfo.objects.get(uid=user_id)
    std_user_info['avatar'] = user_info.avatar
    std_user_info['name'] = user_info.user_name
    std_user_info['description'] = user_info.user_introduction
    std_user_info['email'] = user_info.email_address
    std_user_info['sex'] = user_info.sex
    std_user_info['age'] = user_info.age
    std_user_info['star'] = user_info.credit
    return std_user_info


def get_visit_info(user_id):  # 传入用户id,返回该用户最近浏览的项目
    return UserVisitRecord.objects.filter(uid=user_id)

def get_user_activity(user_id):
    """
    获得用户最近十条活动记录
    :param user_id:
    :param flag:
    :return:
    发布项目，加入项目，上传数据，审核数据
    """

    # if flag:
    #     activity_list = ProjectInfo.objects.filter(publisher = user_id).order_by('-publish_time')[:10]
    #     activity_list = list(map(lambda activity:{
    #         'date':str(utc_to_shanghai(activity.publish_time, "%Y-%m-%d")),
    #         'type': 'release',
    #         'project':activity.projection_name
    #     },activity_list))
    #
    # else:
    #     # 时间排序
    #     SQL = """select distinct A.uid_id ,C.projection_name,date(A.data_time,'localtime') as time
    #              from project_datainfo A,project_projectimage B,project_projectinfo C
    #              where A.data_id = B.data_id_id and B.pid_id = C.pid and A.uid_id = {}
    #              order by time desc
    #              """.format(user_id)load
    #     cursor = connection.cursor()
    #     cursor.execute(SQL)
    #     result_list = cursor.fetchall()[:10]
    #
    #     upload_activity_list = list(map(lambda activity:{
    #         'project': activity[1],
    #         'date':activity[2],
    #         'type':'upload',
    #     },result_list))
    #
    #     join_activity_list = UserProjectAuthority.objects.filter(uid = user_id,authority = 3).order_by('-register_time')[:10]
    #     join_activity_list = list(map(lambda activity:{
    #         'date':str(utc_to_shanghai(activity.register_time,"%Y-%m-%d")),
    #         'type':'join',
    #         'project':activity.pid.projection_name
    #     },join_activity_list))
    #
    #     activity_list = upload_activity_list+join_activity_list
    #     activity_list.sort(key = lambda k:(k.get('date',0)),reverse = True)
    #     activity_list = activity_list[:10]
    SQL = """
    select *
    from 
     (select A.uid_id ,C.projection_name,date(A.data_time,'localtime') as time1,cast('upload' as 'varchar') as type1, C.pid as pid
      from project_datainfo A,project_projectimage B,project_projectinfo C
      where A.data_id = B.data_id_id and B.pid_id = C.pid and A.uid_id = {}
      union all
      select D.uid_id,E.projection_name,date(D.register_time,'localtime') as time1,cast('join' as 'varchar') as type1, E.pid as pid
      from project_userprojectauthority D, project_projectinfo E
      where D.uid_id = {} and D.authority = 3 and D.pid_id = E.pid
      union all
      select F.uid_id,G.projection_name,date(F.register_time,'localtime') as time1,cast('assist' as 'varchar') as type1, G.pid as pid
      from project_userprojectauthority F,project_projectinfo G
      where F.uid_id = {} and F.authority = 2 and F.pid_id = G.pid
      union all
      select H.publisher_id,H.projection_name,date(H.publish_time,'localtime') as time1, cast('release' as 'varchar') as type1, H.pid as pid 
      from project_projectinfo H
      where H.publisher_id = {}
      ) as temp_table
    order by temp_table.time1 desc
    limit 10
    """.format(user_id,user_id,user_id,user_id)

    cursor = connection.cursor()
    cursor.execute(SQL)
    activities = cursor.fetchall()

    activity_list = list(map(lambda activity:{
        'date':activity[2],
        'type':activity[3],
        'project':activity[1],
        'id':activity[4]
    },activities))

    return activity_list



def get_upload_data(user_id):  # 传入用户名，返回该用户每天上传用户的数据
    # 返回格式 字典{日期：次数}
    user_data_info = {}

    SQL = """select data_id,date(A.data_time,'localtime') as time,count(*) as count
             from Project_datainfo A
             where uid_id = {} 
             group by time
             order by time
             """.format(user_id)
    dict_list = DataInfo.objects.raw(SQL)

    for dict in dict_list:
        user_data_info[dict.time] = dict.count

    return user_data_info


def get_user_project(user_id):  # 获取用户所有参与的项目 如果flag True 是查询发布项目

    # flag为false 查询参与项目
    r_projects = []
    p_projects = []
    a_projects = []

    project_data = UserProjectAuthority.objects.filter(uid = user_id)
    project_data = list(map(lambda item:(item.pid,int(item.authority)),project_data))

    # type_list = ['publisher','assistant','participant']
    for data_tuple in project_data:

        data_info = data_tuple[0]
        time_str = str(utc_to_shanghai(data_info.publish_time, "%Y-%m-%d"))
        year, month, day = map(lambda x: int(x), time_str.split('-'))

        std_user_project = {}
        std_user_project['name'] = data_info.projection_name
        std_user_project['date'] = datetime(year,month,day)
        std_user_project['desc'] = data_info.projection_introduction
        std_user_project['area'] = data_info.area.domain_name
        std_user_project['cover'] = data_info.projection_image
        std_user_project['id'] = data_info.pid
        # std_user_project['type'] = type_list[int(data_tuple[1])-1]

        # std_user_project['url'] = data_info.url
        if data_tuple[1] == 1:
            r_projects.append(std_user_project)
        elif data_tuple[1] == 2:
            a_projects.append(std_user_project)
        elif data_tuple[1] == 3:
            p_projects.append(std_user_project)

    return r_projects,a_projects,p_projects


def utc_to_shanghai(utc_time_str, local_format):  # 将 UTC时间转化为上海时间
    local_tz = pytz.timezone('Asia/Shanghai')
    local_dt = utc_time_str.astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str
