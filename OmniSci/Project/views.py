import os
import re
import uuid

from django.shortcuts import render
from django.views.generic.base import View

from .models import *
from User.models import UserInfo

from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect

from haystack.views import SearchView
from Project.utils.rebuild import rebuild
from Project.utils.trans_str import transform

base_dir = os.path.dirname(os.path.abspath(__file__))


class Release(View):
    """ 项目发布页面

    Attributes: None

    """

    def get(self, request):
        """ 获取项目发布页面

        判断当前用户是否已登录，如果未登录则返回登录页面，已登录则返回项目发布页面

        Args:
            request

        Returns:
            项目发布页面

        """
        if request.session.get('logged_in'):
            return render(request, 'release_project.html')
        else:
            return HttpResponseRedirect('/user/login/')

    def post(self, request):
        """ 处理项目发布数据

        判断项目名称是否重复，对于合理项目，将数据加入数据库

        Args:
            request 应包含以下几个字段
                project_publisher, project_name, project_category, project_introduction, project_image

        Returns:
            反馈信息页面

        """

        # 创建项目缩略图文件夹
        if not os.path.exists(os.path.join(base_dir, 'static/project_image')):
            os.mkdir(os.path.join(base_dir, 'static/project_image'))

        # 判断登录情况
        if not request.session.get('uid'):
            return render(request, 'info.html', {
                'msg': ["请登录"],
                'title': u'发布失败!'
            })

        if not UserInfo.objects.filter(uid=request.session.get('uid')).exists():
            return render(request, 'info.html', {
                'msg': ["请登录"],
                'title': u'发布失败!'
            })

        user = UserInfo.objects.filter(uid=request.session.get('uid')).first()

        name = request.POST.get('project_name')
        category = request.POST.get('project_category')
        introduction = request.POST.get('project_introduction')
        need_data = request.POST.get('project_label')

        # 判断项目信息填写状况
        if not name or not category or not introduction or not need_data:
            return render(request, 'info.html', {
                'msg': ["填写信息不完整"],
                'title': u'发布失败!'
            })

        if len(name) > 30 or len(introduction) > 2000 or len(need_data) > 2000 or\
                len(request.POST.get('user_ai_url', '')) > 200:
            return render(request, 'info.html', {
                'msg': ["填写信息过长"],
                'title': u'发布失败!'
            })

        if len([item for item in re.split(r'[\s,，]', need_data) if item]) <= 0:
            return render(request, 'info.html', {
                'msg': ["请填写有效数据标签"],
                'title': u'发布失败!'
            })

        if category == "动物":
            model = 'http://114.116.29.7/project/submit/type=animal/'
        elif category == "水果":
            model = 'http://114.116.29.7/project/submit/type=fruit/'
        elif category == "植物":
            model = 'http://114.116.29.7/project/submit/type=tree/'
        else:
            model = 'null'

        if request.POST.get('user_ai_url'):
            model = request.POST.get('user_ai_url')

        # 判断领域是否存在
        category_id = DomainInfo.objects.filter(domain_name=category)
        if len(category_id) <= 0:
            return render(request, 'info.html', {
                'msg': ["项目领域不存在"],
                'title': u'发布失败!'
            })

        # 判断用户是否上传项目缩略图
        image = 'project_image/default.png'
        if request.FILES.get('project_image'):
            img = request.FILES['project_image']

            postfix = img.name[img.name.rfind('.'):]
            if postfix not in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
                return render(request, 'info.html', {
                    'msg': ["项目缩略图格式错误"],
                    'title': u'发布失败!'
                })
            image = os.path.join('project_image', '{}{}'.format(uuid.uuid1(), postfix))

            with open(os.path.join(base_dir, 'static', image), 'wb') as file:
                for chunk in img.chunks():
                    file.write(chunk)

        # 存储项目信息
        ProjectInfo(
            projection_name=transform(name),
            projection_introduction=transform(introduction),
            area=category_id[0],
            publisher=user,
            projection_image='/static/' + image,
            need_data=need_data,
            model=model
        ).save()

        # 添加发布者权限
        UserProjectAuthority(
            uid=user,
            pid=ProjectInfo.objects.last(),
            authority=1
        ).save()

        return render(request, 'info.html', {
            'msg': [],
            'title': u'发布成功!'
        })


def get_domain_projects():
    """ 获取数据搜索页面

    Args:
        request

    Returns:
        返回项目详情页面需要的数据(JSON格式)，例如：
        {
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
        }
    """
    data = {}
    cursor = connection.cursor()
    # 获取热门领域 按领域内的项目数排序
    cursor.execute("""
               select 
                   A.aid,
                   A.domain_name
               from
                   Project_domaininfo A
               left join Project_projectinfo B on A.aid = B.area_id
               group by A.aid
               order by count(*) desc
               limit 5
           """)

    key = ['aid', 'domain_name']
    data['domain'] = [dict(zip(key, item)) for item in cursor.fetchall()]

    # 获取热门项目
    cursor.execute("""
               select 
                   A.pid,
                   A.projection_name,
                   date(A.publish_time,'localtime'),
                   A.projection_image
               from 
                   Project_projectinfo A
               left join Project_projectimage B on A.pid = B.pid_id
               group by A.pid
               order by count(*) desc
               limit 6
           """)

    key = ['pid', 'projection_name', 'publish_time', 'projection_image']
    data['projects'] = [dict(zip(key, item)) for item in cursor.fetchall()]

    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

    for dic in data['projects']:
        date = dic['publish_time'].split('-')
        dic['publish_time'] = '{} {} {}'.format(date[2], month[int(date[1]) - 1], date[0])

    return data


# class Search(View):
#
#     def post(self,request):
#         # 搜索内容
#         # TODO 能否找到搜索内容的上位词或者下位词
#         # TODO 考虑中文分词
#         content = request.POST['content']
#         result = {}
#
#
#
#         return render(request, 'project_detail.html')


def search(request):
    """ 获数据搜索页面所需数据

    Args:
        request

    Returns:
        返回数据搜索页面需要的数据(JSON格式)，例如：
        {
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
        }

    """
    return JsonResponse(get_domain_projects())


class MySearchView(SearchView):
    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()

        try:
            self.query = self.get_query()
            self.results = self.get_results()
            return self.create_response()
        except ValueError:
            self.query = self.get_query()
            self.results = self.get_results()
            rebuild()
            return self.create_response()

def mobile(request,pid):
    """
    :param request:
    :return:
    """
    # TODO 身份验证


    # p_data_list = [
    #     {
    #         'uploader':'Mingming',
    #         'tag':'antelope',
    #         'url':'/static/project_image/antelope_1.jpg',
    #     },
    #     {
    #         'uploader': 'Li Lei',
    #         'tag': 'banana',
    #         'url': '/static/project_image/banana_0.jpg',
    #     },
    #     {
    #         'uploader': 'Christine',
    #         'tag': 'apple',
    #         'url': '/static/project_image/apple_0.jpg',
    #     }
    # ]
    # data={
    #     'pid':pid,
    #     'p_name': '华北鹿属动物图鉴',
    #     'p_publisher': 'lingling',
    #     'p_time': '2019-5-8',
    #     'p_introduction': 'Nothing to show~~~',
    #     'p_data': p_data_list,
    #     'labels':['鹿','鼠','牛']
    # }
    cursor = connection.cursor()

    # 项目基本信息
    SQL = """
    select A.pid,
        A.projection_name,
        date(A.publish_time,'localtime'),
        A.projection_introduction,
        A.need_data,
        A.projection_image,
        case when A.publisher_id is null then 'null' else B.user_name end,
        case when A.publisher_id is null then null else B.avatar end
    from Project_projectinfo A
    left join User_userinfo B on A.publisher_id = B.uid
    where A.pid = {}
    """.format(pid)
    cursor.execute(SQL)

    key = ['pid','p_name','p_time','p_introduction','p_need_data','p_image','p_publisher','p_avatar']
    data = dict(zip(key,cursor.fetchone()))

    month = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]

    date = data['p_time'].split('-')

    data['p_time'] = "{}th {} > {}".format(date[2], month[int(date[1]) - 1], date[0])

    data['p_need_data'] = data['p_need_data'] if data['p_need_data'] else ""
    data['labels'] = [item for item in re.split(r'[\s,，]', data['p_need_data']) if item]

    # 项目数据
    SQL = """
    select A.data_id,
           A.data_path,
           A.data_name,
           date(A.data_time,'localtime'),
           case when A.uid_id is null then 'null' else C.user_name end
    from Project_datainfo A,
           Project_projectimage B
    left join User_userinfo C on A.uid_id = C.uid
    where B.pid_id = {} and B.data_id_id = A.data_id and B.verified = 1
    limit 9
    """.format(pid)
    cursor.execute(SQL)

    key = ['d_id','url','tag','upload_time','uploader']
    p_data_list = list(map(lambda item:dict(zip(key,item)),cursor.fetchall()))
    data['p_data'] = p_data_list

    data['authority'] = 4
    # 判断当前用户权限，4: 无权限 3: 参与志愿者 2: 协助志愿者 1: 项目发布者
    if request.session.get("uid"):
        user = UserInfo.objects.filter(uid=request.session["uid"])[0]
        authorities = UserProjectAuthority.objects.filter(uid=user, pid=pid)
        if len(authorities) > 0:
            data['authority'] = authorities[0].authority

    return render(request, 'project_mobile.html',data)


################################################ Debug 专用 ##############################################

def m_category_debug(request):
    return render(request, 'project_category_mobile.html')

def m_info_debug(request):
    return render(request, 'info_mobile.html')

def detail_debug(request):
    return render(request, 'project_detail.html')

