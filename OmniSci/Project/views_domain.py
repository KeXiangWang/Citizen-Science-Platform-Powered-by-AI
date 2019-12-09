import os
import math

from .models import *
from User.utils import is_pc
from .views import get_domain_projects

from django.shortcuts import render

from django.db import connection
from django.http import JsonResponse
from django.views.generic.base import View

base_dir = os.path.dirname(os.path.abspath(__file__))


class Domain(View):

    def get(self, request, domain_name):

        pc = is_pc(request.META['HTTP_USER_AGENT'])

        data = {'domain_name': str(domain_name)}
        cursor = connection.cursor()

        if domain_name == '所有项目':
            if pc:
                cursor.execute("""
                    select
                        count(*)
                    from
                        Project_projectinfo A
                """)
            else:
                cursor.execute("""
                    select
                        A.pid,
                        A.projection_name,
                        date(A.publish_time, 'localtime'),
                        A.projection_image,
                        A.projection_introduction,
                        case when A.publisher_id is null then 'null' else C.user_name end
                    from
                        Project_projectinfo A
                    left join Project_projectimage B on A.pid = B.pid_id
                    left join User_userinfo C on A.publisher_id = C.uid
                    group by A.pid
                    order by count(*) desc
                    limit 20
                """)
        else:
            if not DomainInfo.objects.filter(domain_name=domain_name).exists():
                return render(request, 'info.html' if pc else 'info_mobile.html', {
                    'msg': ["领域不存在"],
                    'title': u'访问错误!'
                })

            domain = DomainInfo.objects.filter(domain_name=domain_name).first()

            if pc:
                cursor.execute("""
                    select
                        count(*)
                    from
                        Project_projectinfo A
                    where A.area_id = {}
                """.format(domain.aid))
            else:
                cursor.execute("""
                    select
                        A.pid,
                        A.projection_name,
                        date(A.publish_time, 'localtime'),
                        A.projection_image,
                        A.projection_introduction,
                        case when A.publisher_id is null then 'null' else C.user_name end
                    from
                        Project_projectinfo A
                    left join Project_projectimage B on A.pid = B.pid_id
                    left join User_userinfo C on A.publisher_id = C.uid
                    where A.area_id = {}
                    group by A.pid
                    order by count(*) desc
                    limit 20
                """.format(domain.aid))

        if pc:
            data['page_cnt'] = math.ceil(cursor.fetchone()[0] / 6)
            data.update(get_domain_projects())
        else:
            key = ['pid', 'projection_name', 'publish_time', 'projection_image', 'projection_introduction', 'user_name']
            data['domain_project'] = [dict(zip(key, item)) for item in cursor.fetchall()]

        return render(request, 'project_category.html' if pc else 'project_category_mobile.html', data)

    def post(self, request, domain_name):
        page_cnt = request.POST.get('page_cnt')
        proejct_num = 6 if is_pc(request.META['HTTP_USER_AGENT']) else 20

        if not page_cnt:
            return JsonResponse({
                'domain_project': [],
                'total_project': 0
            })

        cursor = connection.cursor()
        data = {}

        if domain_name == '所有项目':
            cursor.execute("""
                select
                    A.pid,
                    A.projection_name,
                    date(A.publish_time, 'localtime'),
                    A.projection_image,
                    A.projection_introduction,
                    case when A.publisher_id is null then 'null' else C.user_name end
                from
                    Project_projectinfo A
                left join Project_projectimage B on A.pid = B.pid_id
                left join User_userinfo C on A.publisher_id = C.uid
                group by A.pid
                order by count(*) desc
                limit {}, {}
            """.format((int(page_cnt) * proejct_num), proejct_num))
            data['total_project'] = ProjectInfo.objects.all().count()
        else:
            if not DomainInfo.objects.filter(domain_name=domain_name).exists():
                data = {
                    'domain_project': [],
                    'total_project': 0
                }

                return JsonResponse(data)

            domain = DomainInfo.objects.filter(domain_name=domain_name).first()

            cursor.execute("""
                select
                    A.pid,
                    A.projection_name,
                    date(A.publish_time, 'localtime'),
                    A.projection_image,
                    A.projection_introduction,
                    case when A.publisher_id is null then 'null' else C.user_name end
                from
                    Project_projectinfo A
                left join Project_projectimage B on A.pid = B.pid_id
                left join User_userinfo C on A.publisher_id = C.uid
                where A.area_id = {}
                group by A.pid
                order by count(*) desc
                limit {}, {}
            """.format(domain.aid, (int(page_cnt) * proejct_num), proejct_num))

            data['total_project'] = ProjectInfo.objects.filter(area_id=domain).count()

        key = ['pid', 'projection_name', 'publish_time', 'projection_image', 'projection_introduction', 'user_name']

        data['domain_project'] = [dict(zip(key, item)) for item in cursor.fetchall()]

        return JsonResponse(data)
