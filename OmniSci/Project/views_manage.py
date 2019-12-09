import os
import re
import zipstream

from .models import *
from User.models import UserInfo

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse


def panel(pid):
    """ 获取项目管理信息

    Args:
        pid

    Returns:

        TODO 填一下？
    """
    province_list = ('北京', '天津',
                     '上海', '重庆',
                     '河北', '河南',
                     '云南', '辽宁',
                     '黑龙江', '湖南',
                     '安徽', '山东',
                     '新疆', '江苏',
                     '浙江', '江西',
                     '湖北', '广西',
                     '甘肃', '山西',
                     '内蒙古', '陕西',
                     '吉林', '福建',
                     '贵州', '广东',
                     '青海', '西藏',
                     '四川', '宁夏',
                     '海南', '台湾',
                     '香港', '澳门',
                     '南海诸岛')
    cursor = connection.cursor()

    # 最近上传数据的志愿者
    SQL = """select C.uid,
                    B.verified,
                    datetime(A.data_time,'localtime') as upload_time,C.user_name
             from Project_datainfo A,Project_projectimage B,User_userinfo C
             where A.data_id = B.data_id_id and A.uid_id = C.uid and  B.pid_id = {}
             order by upload_time desc
          """.format(pid)
    cursor.execute(SQL)
    p_partner = cursor.fetchall()

    # 上传量统计
    SQL = """select round(julianday('now','localtime','start of day')-julianday(A.data_time,'localtime','start of day')) as upload_date,count(*) as count
             from project_datainfo A,project_projectimage B
             where A.data_id = B.data_id_id and upload_date < 30 and B.pid_id = {}
             group by upload_date
             order by upload_date
                  """.format(pid)
    cursor.execute(SQL)
    frequency = cursor.fetchall()

    p_data = [0] * 30
    for daily_record in frequency:
        p_data[29 - int(daily_record[0])] = daily_record[1]

    # 项目详情 如果项目不存在会报错 模型id可以为空，领域id非空
    SQL = """select A.pid,
             A.projection_name,
             date(A.publish_time,'localtime'),
             A.projection_introduction,
             A.projection_image,
             C.domain_name,
             A.model
             from project_projectinfo A,project_domaininfo C
             where A.area_id = C.aid and A.pid = {}
            """.format(pid)

    cursor.execute(SQL)
    project_info = cursor.fetchone()

    label = ['pid', 'p_name', 'p_time', 'p_intro', 'p_image', 'p_area', 'p_model']
    data = dict(zip(label, project_info))

    # 截断过长评论
    # if len(data.get('p_intro')) <= 200:
    #     data['p_intro_200'] = data.get('p_intro')
    #     data['p_intro_other'] = ''
    # else:
    #     data['p_intro_200'] = data.get('p_intro')[0:200]
    #     data['p_intro_other'] = data.get('p_intro')[200:]
    # data['p_intro'] = json.dumps(data['p_intro'])  # 不删，传到前端有用

    # 今日上传量
    SQL = """select count(*)
             from Project_datainfo A,Project_projectimage B
             where A.data_id = B.data_id_id and B.pid_id = {}
             and strftime('%Y-%m-%d',A.data_time,'localtime') = strftime('%Y-%m-%d','now','localtime')
             """.format(pid)
    cursor.execute(SQL)
    today_upload = cursor.fetchone()

    data['today_people'] = today_upload[0]
    data['all_people'] = DataInfo.objects.filter(projectimage__pid=pid).values('uid').distinct().count()
    data['data_quantity'] = ProjectImage.objects.filter(pid=pid).count()

    # 上传数据的地理位置统计
    SQL = """
        select A.data_province, count(*) as num
        from project_datainfo A, project_projectinfo B, project_projectimage C
        where A.data_id = C.data_id_id and B.pid = C.pid_id and B.pid ={} and date('now','localtime',{}) <= date(A.data_time,'localtime') and A.data_province is not null
        group by A.data_province
        order by num desc
        """

    cursor.execute(SQL.format(pid, "\'-7 day\'"))
    result = cursor.fetchall()
    # province_data_week = [[_[0], _[1]] for _ in cursor.fetchall()]
    province_data_week = []
    week_province_list = []
    for location in result:
        province_data_week.append([location[0], int(location[1])])
        week_province_list.append(location[0])
    for pro in province_list:
        if not pro in week_province_list:
            province_data_week.append([pro, 0])
    max_week = province_data_week[0][1] if province_data_week != [] else 0

    cursor.execute(SQL.format(pid, "\'-1 month\'"))
    result = cursor.fetchall()
    # province_data_month = [[_[0], _[1]] for _ in cursor.fetchall()]
    province_data_month = []
    month_province_list = []
    for location in result:
        province_data_month.append([location[0], int(location[1])])
        month_province_list.append(location[0])
    for pro in province_list:
        if not pro in month_province_list:
            province_data_month.append([pro, 0])
    max_month = province_data_month[0][1] if province_data_month != [] else 0

    cursor.execute(SQL.format(pid, "\'-1 year\'"))
    result = cursor.fetchall()
    # province_data_year = [[_[0], _[1]] for _ in cursor.fetchall()]
    province_data_year = []
    year_province_list = []
    for location in result:
        province_data_year.append([location[0], int(location[1])])
        year_province_list.append(location[0])
    for pro in province_list:
        if not pro in year_province_list:
            province_data_year.append([pro, 0])
    max_year = province_data_year[0][1] if province_data_year != [] else 0

    data['province_data_week'] = province_data_week
    data['province_data_month'] = province_data_month
    data['province_data_year'] = province_data_year

    data['max_week'] = max_week
    data['max_month'] = max_month
    data['max_year'] = max_year

    # 截断过长志愿者列表
    data['p_partner'] = p_partner
    if len(data.get('p_partner')) <= 8:
        data['p_partner8'] = data.get('p_partner')
        data['p_partner_other'] = ''
    else:
        data['p_partner8'] = data.get('p_partner')[0:7]
        data['p_partner_other'] = data.get('p_partner')[8:]

    data['p_data'] = p_data

    # data['province_data_week'] = [['安徽', 1], ['北京', 2]]  # 二维列表，省份为
    # # '北京''天津''上海''重庆''河北''河南''云南''辽宁''黑龙江''湖南''安徽''山东''新疆''江苏'
    # # '浙江' '江西''湖北''广西''甘肃''山西''内蒙古''陕西''吉林''福建''贵州''广东''青海''西藏'
    # # '四川''宁夏''海南''台湾''香港''澳门'
    # # 数字是数据提交量
    # data['max_week'] = 2  # 上面二维列表中所有数字的最大值
    # data['province_data_month'] = [['安徽', 4], ['北京', 25]]
    # data['max_month'] = 25
    # data['province_data_year'] = [['安徽', 122], ['北京', 222]]
    # data['max_year'] = 222
    #
    return data


def update(request):
    """ 更新项目管理信息

    更新项目介绍

    Args:
        request

    """

    # 判断信息
    pid = request.POST.get('pid')
    data = request.POST.get('text')
    key = request.POST.get('key')
    if not pid or not data or not key:
        return HttpResponse("Fail")
    # 判断权限
    if request.session.get('logged_in', None) is not True:
        return render(request, 'User/login.html')
    elif not UserProjectAuthority.objects.filter(uid=request.session.get('uid', None), pid=pid, authority=1).exists():
        return render(request, 'info.html',
                      {'msg': ['Permission denied, you are not authorized!'], 'title': 'Access Failed'})
    # 更新项目内容
    if key == 'introduction':
        ProjectInfo.objects.filter(pid=pid).update(projection_introduction=data)
    elif key == 'model':
        ProjectInfo.objects.filter(pid=pid).update(model=data)
    elif key == 'labels':
        labels = [item for item in re.split(r'[\s,，]', data) if item]
        if len(labels) <= 0:
            return HttpResponse("Fail")
        ProjectInfo.objects.filter(pid=pid).update(need_data=data)

    return HttpResponse("Succeed")


def updateModel(request):
    pid = request.POST.get('pid')
    data = request.POST.get('model')
    print(data)
    return HttpResponse("Succeed")


class ZipUtilities:
    zip_file = None

    def __init__(self):
        self.zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)

    def toZip(self, file, name):
        if os.path.isfile(file):
            self.zip_file.write(file, arcname=os.path.basename(file))
        else:
            self.addFolderToZip(file, name)

    def addFolderToZip(self, folder, name):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                self.zip_file.write(full_path, arcname=os.path.join(name, os.path.basename(full_path)))
            elif os.path.isdir(full_path):
                self.addFolderToZip(full_path, os.path.join(name, os.path.basename(full_path)))

    def close(self):
        if self.zip_file:
            self.zip_file.close()


def download(request, pid):
    # 下载数据后端逻辑
    # 根据pid判断该用户有没有下载的权限
    # TODO 换用装饰器
    if request.session.get('logged_in', None) is not True:
        return render(request, 'User/login.html')
    elif not UserProjectAuthority.objects.filter(uid=request.session.get('uid', None), pid=pid, authority=1).exists():
        return render(request, 'info.html',
                      {'msg': ['Permission denied, you are not authorized!'], 'title': 'Access Failed'})

    # 项目所有上传数据的url表
    cursor = connection.cursor()
    SQL = """select A.data_path
                 from project_datainfo A,project_projectimage B
                 where A.data_id = B.data_id_id and B.pid_id = {}
                 """.format(pid)
    cursor.execute(SQL)
    urls = [('Project' + item[0]) for item in cursor.fetchall()]

    utilities = ZipUtilities()
    for i in urls:
        utilities.toZip(i, 'temp.zip')
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('Project' + str(pid) + ".zip")
    return response


def delete(request):
    # TODO 判断是否有权限 之前的update最好也加一下
    pid = request.POST.get('pid')
    if request.session.get('logged_in', None) is not True:
        return render(request, 'User/login.html')
    elif not UserProjectAuthority.objects.filter(uid=request.session.get('uid', None), pid=pid, authority=1).exists():
        return render(request, 'info.html',
                      {'msg': ['Permission denied, you are not authorized!'], 'title': 'Access Failed'})

    # 根据pid来删除项目
    project = ProjectInfo.objects.get(pid=pid)
    domain = project.area
    project.delete()

    return HttpResponse(domain.domain_name)  # 将当前删除这个项目的领域返回，便于跳转


def add_authority(request, pid):
    msg = {'result': False}

    # 判断登录情况
    if not request.session.get("uid"):
        msg['msg'] = 'Please login first'
        return JsonResponse(msg)

    project = ProjectInfo.objects.filter(pid=pid)[0]
    user = UserInfo.objects.filter(uid=request.session["uid"])[0]
    authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

    if len(authorities) <= 0 or authorities[0].authority > 1:
        msg['msg'] = 'Insufficient authority'
        return JsonResponse(msg)

    mail = request.POST.get('mail')

    if not mail:
        msg['msg'] = 'Insufficient information'
        return JsonResponse(msg)

    if not UserInfo.objects.filter(email_address=mail).exists():
        msg['msg'] = 'User not exist'
        return JsonResponse(msg)

    volunteer = UserInfo.objects.filter(email_address=mail).first()

    volunteer_authorities = UserProjectAuthority.objects.filter(uid=volunteer, pid=project)

    if len(volunteer_authorities) <= 0:
        msg['msg'] = 'User has not participate'
        return JsonResponse(msg)

    if volunteer_authorities[0].authority != 3:
        msg['msg'] = 'The user is not a volunteer'
        return JsonResponse(msg)

    UserProjectAuthority.objects.filter(uid=volunteer, pid=project).update(authority=2)
    msg['result'] = True
    msg['msg'] = 'Add successfully'
    msg['user'] = {'uid': volunteer.uid, 'user_name': volunteer.user_name, 'email_address': volunteer.email_address}

    return JsonResponse(msg)


def remove_authority(request, pid):
    msg = {'result': False}

    # 判断登录情况
    if not request.session.get("uid"):
        msg['msg'] = 'Please login first'
        return JsonResponse(msg)

    project = ProjectInfo.objects.filter(pid=pid)[0]
    user = UserInfo.objects.filter(uid=request.session["uid"])[0]
    authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

    if len(authorities) <= 0 or authorities[0].authority > 1:
        msg['msg'] = 'Insufficient authority'
        return JsonResponse(msg)

    uid = request.POST.get('uid')

    if not uid:
        msg['msg'] = 'Insufficient information'
        return JsonResponse(msg)

    if not UserInfo.objects.filter(uid=uid).exists():
        msg['msg'] = 'User not exist'
        return JsonResponse(msg)

    volunteer = UserInfo.objects.filter(uid=uid).first()

    volunteer_authorities = UserProjectAuthority.objects.filter(uid=volunteer, pid=project)

    if len(volunteer_authorities) <= 0:
        msg['msg'] = 'User has not participate'
        return JsonResponse(msg)

    if volunteer_authorities[0].authority != 2:
        msg['msg'] = 'The user is not an administrator'
        return JsonResponse(msg)

    UserProjectAuthority.objects.filter(uid=volunteer, pid=project).update(authority=3)
    msg['result'] = True
    msg['msg'] = 'Remove successfully'

    return JsonResponse(msg)
