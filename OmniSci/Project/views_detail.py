import os
import re
import math
import uuid
import requests

from .models import *
from User.models import UserInfo

from .views import get_domain_projects
from .views_manage import panel

from User.utils import is_pc
from Project.utils.gisHelper import GisHelper

from django.shortcuts import render
from django.views.generic.base import View

from django.db import connection
from django.http import JsonResponse

base_dir = os.path.dirname(os.path.abspath(__file__))


def page_cnt(pid, verified):
    """ 获取页数

    Args:

        pid

        verified

    Returns:
        {
            'page_cnt': int
        }

    """
    cursor = connection.cursor()

    cursor.execute("""
        select 
            count(*)
        from 
            Project_projectimage A
        where A.pid_id = {} and A.verified = {}
    """.format(pid, verified))

    return {'page_cnt': math.ceil(cursor.fetchone()[0] / 9)}


class Detail(View):

    def get(self, request, pid):
        """ 获取项目详情页面

        Args:
            request

            pid

        Returns:
            返回项目详情页面需要的数据(JSON格式)，例如：
            {
                'project':
                    {
                        pid: ...
                    }
                'domain':
                    [
                        {
                            aid: ...
                        }
                    ]
                'projects':
                    [
                        {
                            pid: ...
                        }
                    ]
                'join': bool
                'manage': bool
                'need_data': bool
                'page_cnt': int
                'issue_page_cnt': int
            }

        """
        pc = is_pc(request.META['HTTP_USER_AGENT'])
        if not ProjectInfo.objects.filter(pid=pid).exists():
            return render(request, 'info.html' if pc else 'info_mobile.html', {
                'msg': ["项目不存在"],
                'title': u'访问错误!'
            })

        project = ProjectInfo.objects.filter(pid=pid).first()

        data = {'authority': 4}
        # 判断当前用户权限，4: 无权限 3: 参与志愿者 2: 协助志愿者 1: 项目发布者
        if request.session.get("uid"):
            user = UserInfo.objects.filter(uid=request.session["uid"])[0]
            authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)
            if len(authorities) > 0:
                data['authority'] = authorities[0].authority

        cursor = connection.cursor()

        cursor.execute("""
            select 
                A.pid,
                A.projection_name,
                A.projection_image,
                date(A.publish_time,'localtime'),
                A.projection_introduction,
                A.need_data,
                case when A.publisher_id is null then 'null' else B.user_name end,
                case when A.publisher_id is null then '/static/images_mobile/default_avatar.jpeg' else B.avatar end
            from 
                Project_projectinfo A
            left join User_userinfo B on A.publisher_id = B.uid
            where A.pid = {}
        """.format(pid))

        key = ['pid', 'projection_name', 'projection_image', 'publish_time',
               'projection_introduction', 'need_data', 'user_name', 'user_avatar']
        data['project'] = dict(zip(key, cursor.fetchone()))

        month = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]

        date = data['project']['publish_time'].split('-')

        data['project']['publish_time'] = "{}th {} > {}".format(date[2], month[int(date[1]) - 1], date[0])

        data['project']['need_data'] = data['project']['need_data'] if data['project']['need_data'] else ""
        data['labels'] = [item for item in re.split(r'[\s,，]', data['project']['need_data']) if item]

        if not pc:
            cursor.execute("""
                select 
                    A.data_path,
                    A.data_name,
                    case when A.uid_id is null then 'null' else C.user_name end
                from 
                    Project_datainfo A,
                    Project_projectimage B
                left join User_userinfo C on A.uid_id = C.uid
                where B.pid_id = {} and B.data_id_id = A.data_id and B.verified = 1
                limit 9
            """.format(pid))

            key = ['data_path', 'data_name', 'user_name',]
            data['data'] = [dict(zip(key, item)) for item in cursor.fetchall()]

            return render(request, 'project_detail_mobile.html', data)

        # 获取项目数据 根据权限获取 协助志愿者和项目发布者看全部 其余人只给看9张（第一页）
        if data['authority'] < 3:
            data.update(page_cnt(pid, 1))
        else:
            data['page_cnt'] = 1

        cursor.execute("""
            select 
                count(*)
            from 
                Project_projectissue B
            where B.pid_id = {}
        """.format(pid))

        data['issue_page_cnt'] = math.ceil(cursor.fetchone()[0] / 5)

        cursor.execute("""
            select 
                A.uid,
                A.user_name,
                A.email_address
            from 
                User_userinfo A,
                Project_userprojectauthority B
            where B.pid_id = {} and B.uid_id = A.uid and B.authority = 2
        """.format(pid))

        key = ['uid', 'user_name', 'email_address']
        data['assistant'] = [dict(zip(key, item)) for item in cursor.fetchall()]

        data.update(get_domain_projects())

        if data['authority'] < 2:
            data.update(panel(pid))

        return render(request, 'project_detail.html', data)

    def post(self, request, pid, page_num, verified):
        """ 获取项目数据（一页）

        Args:
            request

            pid

            page_num

        Returns:
            返回项目详情页面需要的数据(JSON格式)，例如：
            [
                {
                    'data_path': ...
                    'data_time': ...
                    'user_name': ...
                    'verified':  ...
                }
            ]
        """
        if page_num > 1:
            msg = {'result': False}
            # 判断登录情况
            if not request.session.get("uid"):
                msg['msg'] = 'Please login firstly'
                return JsonResponse(msg)

            project = ProjectInfo.objects.filter(pid=pid)[0]
            user = UserInfo.objects.filter(uid=request.session["uid"])[0]
            authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

            # 判断权限
            if len(authorities) < 0 or authorities[0].authority > 2:
                msg['msg'] = 'You don\'t have authority'
                return JsonResponse(msg)

        cursor = connection.cursor()

        cursor.execute("""
            select 
                A.data_id,
                A.data_path,
                A.data_name,
                date(A.data_time,'localtime'),
                case when A.uid_id is null then 'null' else C.user_name end,
                B.verified
            from 
                Project_datainfo A,
                Project_projectimage B
            left join User_userinfo C on A.uid_id = C.uid
            where B.pid_id = {} and B.data_id_id = A.data_id and B.verified = {}
            limit {}, 9
        """.format(pid, verified, (page_num - 1) * 9))

        key = ['data_id', 'data_path', 'data_name', 'data_time', 'user_name', 'verified']
        data = {'data': [dict(zip(key, item)) for item in cursor.fetchall()]}

        return JsonResponse(data)


def get_page_cnt(request, pid, verified):
    """ 获取页数

    Args:
        request

        pid

        verified

    Returns:
        {
            'page_cnt': int
        }

    """

    cursor = connection.cursor()

    cursor.execute("""
        select 
            count(*)
        from 
            Project_projectimage A
        where A.pid_id = {} and A.verified = {}
    """.format(pid, verified))

    data = {'page_cnt': math.ceil(cursor.fetchone()[0] / 9)}

    return JsonResponse(data)


def user_join(request, pid):
    """ 处理用户加入

    判断用户信息，用户权限等，修改数据库

    Args:
        request

        pid

    Returns:
        msg:
        {
            'result': true/false,
            'msg': message for join result
        }

    """
    msg = {'result': False}

    # 判断登录情况
    if not request.session.get("uid"):
        msg['msg'] = 'Please login first'
        return JsonResponse(msg)

    project = ProjectInfo.objects.filter(pid=pid)[0]
    user = UserInfo.objects.filter(uid=request.session["uid"])[0]
    authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

    # 判断已有权限 禁止重复参与
    if len(authorities) > 0:
        msg['msg'] = 'Please don\'t participate repeatedly'
        return JsonResponse(msg)

    # 写入新的用户权限信息
    UserProjectAuthority(
        pid=project,
        uid=user,
        authority=3
    ).save()

    msg['result'] = True
    msg['msg'] = 'Participate successfully'

    return JsonResponse(msg)


def filter(province):
    pro = province.replace("省","")
    pro = pro.replace("维吾尔自治区","")
    pro = pro.replace("壮族自治区","")
    pro = pro.replace("回族自治区","")
    pro = pro.replace("自治区","")
    pro = pro.replace("市","")
    pro = pro.replace("特别行政区","")
    return pro


def user_submit(request, pid):
    """ 处理提交

    判断用户信息，用户权限等，修改数据库

    Args:
        request

        pid

    Returns:
        msg:
        {
            'result': true/false,
            'msg': message for submit result
        }

    """
    msg = {'result': False}

    # 判断登录情况
    if not request.session.get("uid"):
        msg['msg'] = 'Please login firstly'
        return JsonResponse(msg)

    project = ProjectInfo.objects.filter(pid=pid)[0]
    user = UserInfo.objects.filter(uid=request.session["uid"])[0]
    authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

    if user.credit <= 0:
        msg['msg'] = 'Evil reputation'
        return JsonResponse(msg)

    # 判断用户对于项目的权限
    if len(authorities) == 0:
        msg['msg'] = 'Please participate project firstly'
        return JsonResponse(msg)

    # 建立存储数据的文件夹
    if not os.path.exists(os.path.join(base_dir, 'static/project_data')):
        os.mkdir(os.path.join(base_dir, 'static/project_data'))

    if not request.FILES.get('image'):
        msg['msg'] = 'Please select an image'
        return JsonResponse(msg)

    data_name = 'null'
    if request.POST.get('label'):
        data_name = request.POST.get('label')

    img = request.FILES['image']

    # 判断数据合理性
    postfix = img.name[img.name.rfind('.'):]
    if postfix not in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
        msg['msg'] = 'Wrong format'
        return JsonResponse(msg)

    image_name = '{}{}'.format(uuid.uuid1(), postfix)
    image = os.path.join('project_data', image_name)

    with open(os.path.join(base_dir, 'static', image), 'wb') as file:
        for chunk in img.chunks():
            file.write(chunk)

    # 获取用户的gis信息
    city = request.POST.get('city')
    province = request.POST.get('province')
    if not city or not province or province == '请选择省份':
        gis_helper = GisHelper()
        ip = gis_helper.fetch_ip(request)
        city, province = gis_helper.query(ip)

    # 写入新数据
    DataInfo.objects.create(
        data_type='image',
        data_name=data_name,
        data_path='/static/' + image,
        data_location=city,
        data_province=filter(province),
        uid=user
    )

    new_data = DataInfo.objects.last()

    # 写入数据项目对应关系
    relation = ProjectImage.objects.create(
        pid=project,
        data_id=new_data,
        verified=0
    )

    if project.model != 'null':
        try:
            file = {
                'image': (
                    image_name,
                    open(os.path.join(base_dir, 'static', image), 'rb')
                )
            }
            result = requests.post(project.model, files=file).json()
        except:
            result = {'result': True}

        if 'result' in result and not result['result']:
            relation.verified = -1
            relation.save()
            msg['data_id'] = new_data.data_id
            msg['msg'] = 'Bad data'
            return JsonResponse(msg)

    if user.credit <= 30:
        relation.verified = -1
        relation.save()
        msg['data_id'] = new_data.data_id
        msg['msg'] = 'Low reputation'
        return JsonResponse(msg)

    relation.save()
    msg['result'] = True
    msg['msg'] = 'Submit successfully'

    return JsonResponse(msg)


def bad_submit(request):
    """ 处理错误提交

    判断数据，修改数据库

    Args:
        request

    Returns:
        msg:
        {
            'result': true/false,
            'msg': message for result
        }

    """

    msg = {'result': False}

    data_id = request.POST.get('data_id')
    option = request.POST.get('option')

    if not data_id or not option:
        msg['msg'] = 'Not enough infomation'
        return JsonResponse(msg)

    if not DataInfo.objects.filter(data_id=data_id).exists():
        msg['msg'] = 'Data not exist'
        return JsonResponse(msg)

    data = DataInfo.objects.filter(data_id=data_id).first()

    if not ProjectImage.objects.filter(data_id=data).exists():
        msg['msg'] = 'Relation not exist'
        return JsonResponse(msg)

    relation = ProjectImage.objects.filter(data_id=data).first()

    if relation.verified != -1:
        msg['msg'] = 'Can not operate this data'
        return JsonResponse(msg)

    if option == 'remove':
        os.remove(base_dir + data.data_path)
        relation.delete()
        data.delete()
    elif option == 'confirm':
        relation.verified = 0
        relation.save()
    else:
        msg['msg'] = 'Wrong Option'
        return JsonResponse(msg)

    msg['result'] = True
    msg['msg'] = 'Succeed'

    return JsonResponse(msg)


def user_audition(request, pid):
    """ 处理审核

   判断用户信息，用户权限等，修改数据库

   Args:
       request

   Returns:
       msg:
       {
           'result': true/false,
           'msg': message for submit result
           'page_cnt': int
       }

   """
    msg = {'result': False}

    # 判断登录情况
    if not request.session.get("uid"):
        msg['msg'] = 'Please login firstly'
        return JsonResponse(msg)

    project = ProjectInfo.objects.filter(pid=pid)[0]
    user = UserInfo.objects.filter(uid=request.session["uid"])[0]
    authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

    # 判断权限
    if len(authorities) < 0 or authorities[0].authority > 2:
        msg['msg'] = 'You don\'t have authority'
        return JsonResponse(msg)

    # 判断表单信息
    data_id = request.POST.get('data_id', None)
    verified = request.POST.get('verified', None)
    option = request.POST.get('option', None)
    if not data_id or not verified or not option:
        msg['msg'] = 'Insufficient information'
        return JsonResponse(msg)

    # 判断操作
    if option not in ['accept', 'decline', 'delete']:
        msg['msg'] = 'Bad option'
        return JsonResponse(msg)

    # 判断数据
    data = DataInfo.objects.filter(data_id=data_id)
    if len(data) <= 0:
        msg['msg'] = 'Data don\'t exist'
        return JsonResponse(msg)

    data = data[0]

    if option == 'accept':
        if verified == '1':
            msg['msg'] = 'Bad option'
            return JsonResponse(msg)
        image = ProjectImage.objects.filter(pid=pid, data_id=data_id)[0]
        if data.uid:
            volunteer = data.uid
            if image.verified == 2:
                volunteer.credit = volunteer.credit + 2
            elif image.verified == 0:
                volunteer.credit = volunteer.credit + 1
            if volunteer.credit > 100:
                volunteer = 100
            volunteer.save()
        image.verified = 1
        image.save()
    elif option == 'decline':
        if verified == '2':
            msg['msg'] = 'Bad option'
            return JsonResponse(msg)
        image = ProjectImage.objects.filter(pid=pid, data_id=data_id)[0]
        if data.uid:
            volunteer = data.uid
            if image.verified == 1:
                volunteer.credit = volunteer.credit - 2
            elif image.verified == 0:
                volunteer.credit = volunteer.credit - 1
            volunteer.save()
        image.verified = 2
        image.save()
    else:
        if verified != '2':
            msg['msg'] = 'Bad option'
            return JsonResponse(msg)
        os.remove(base_dir + data.data_path)
        data.delete()

    msg['result'] = True
    msg.update(page_cnt(pid, verified))

    return JsonResponse(msg)


def user_audition_all(request, pid):
    """ 处理审核

   判断用户信息，用户权限等，修改数据库

   Args:
       request

   Returns:
       msg:
       {
           'result': true/false,
           'msg': message for submit result
           'page_cnt': int
       }

   """
    msg = {'result': False}

    # 判断登录情况
    if not request.session.get("uid"):
        msg['msg'] = 'Please login firstly'
        return JsonResponse(msg)

    project = ProjectInfo.objects.filter(pid=pid)[0]
    user = UserInfo.objects.filter(uid=request.session["uid"])[0]
    authorities = UserProjectAuthority.objects.filter(uid=user, pid=project)

    # 判断权限
    if len(authorities) < 0 or authorities[0].authority > 2:
        msg['msg'] = 'You don\'t have authority'
        return JsonResponse(msg)

    # 判断表单信息
    verified = request.POST.get('verified', None)
    option = request.POST.get('option', None)
    if not verified or not option:
        msg['msg'] = 'Insufficient information'
        return JsonResponse(msg)

    # 判断操作
    if option not in ['accept', 'decline', 'delete']:
        msg['msg'] = 'Bad option'
        return JsonResponse(msg)

    cursor = connection.cursor()

    if option == 'accept':
        if verified == '1':
            msg['msg'] = 'Bad option'
            return JsonResponse(msg)
        cursor.execute("""
           update 
                User_userinfo
            set
                credit = credit + {} * (
                    select
                        count(*)
                    from
                        Project_projectimage A, Project_datainfo B 
                    where A.pid_id = {} and A.verified = {} and A.data_id_id = B.data_id and B.uid_id = User_userinfo.uid
                )
        """.format(1 if verified == '0' else 2, pid, verified))

        cursor.execute("""
            update 
                Project_projectimage
            set
                verified = 1 
            where pid_id = {} and verified = {}
        """.format(pid, verified))

    elif option == 'decline':
        if verified == '2':
            msg['msg'] = 'Bad option'
            return JsonResponse(msg)

        cursor.execute("""
            update 
                User_userinfo
            set
                credit = credit - {} * (
                    select
                        count(*)
                    from
                        Project_projectimage A, Project_datainfo B 
                    where A.pid_id = {} and A.verified = {} and A.data_id_id = B.data_id and B.uid_id = User_userinfo.uid
                )
        """.format(1 if verified == '0' else 2, pid, verified))

        cursor.execute("""
            update 
                Project_projectimage
            set
                verified = 2
            where pid_id = {} and verified = {}
        """.format(pid, verified))

    else:
        if verified != '2':
            msg['msg'] = 'Bad option'
            return JsonResponse(msg)
        cursor.execute("""
            select 
                B.data_path
            from
                Project_projectimage A, Project_datainfo B 
            where A.pid_id = {} and A.verified = 2 and A.data_id_id = B.data_id
        """.format(pid))

        delete_path = [item[0] for item in cursor.fetchall()]

        project = ProjectInfo.objects.get(pid=pid)

        ProjectImage.objects.filter(pid=project, verified=2).delete()

        cursor.execute("""
            delete from 
                Project_datainfo
            where 0 = (
                select
                    count(*)
                from
                    Project_projectimage A
                where A.data_id_id = Project_datainfo.data_id
            )
        """.format(pid))

        for path in delete_path:
            os.remove(base_dir + path)

    msg['result'] = True
    msg.update(page_cnt(pid, verified))

    return JsonResponse(msg)
