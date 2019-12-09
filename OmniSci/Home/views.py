# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect

from Project.models import ProjectInfo
from User.utils import is_pc
import datetime


# Create your views here.

class Home(View):

    def get(self, request):
        """ 获取主页面

        Args:
            request

        Returns:
            主页面

            包含所有热门项目信息的数组，例如：
                [
                    {
                        'pid': xxx,
                        'project_name': xxx
                    },
                    ...
                ]
            包含主要分类项目信息的字典，例如：
                {
                    '植物':
                        [
                            {
                                'pid': xxx,
                                'project_name': xxx
                            },
                            ...
                        ],
                    ...
                }
        """
        if is_pc(request.META['HTTP_USER_AGENT']):
            cursor = connection.cursor()

            cursor.execute("""
                select 
                    A.pid,
                    A.projection_name,
                    date(A.publish_time,'localtime'),
                    A.projection_image,
                    A.projection_introduction, 
                    case when A.publisher_id is null then 'null' else C.user_name end
                from 
                    Project_projectinfo A
                left join Project_projectimage B on A.pid = B.pid_id
                left join User_userinfo C on A.publisher_id = C.uid
                group by A.pid
                order by count(*) desc
                limit 12
            """)

            key = ['pid', 'projection_name', 'publish_time', 'projection_image', 'projection_introduction', 'user_name']
            projects = [dict(zip(key, item)) for item in cursor.fetchall()]

            # 获取项目数多的领域 最多5个
            # question:直接去项目表里筛选领域会不会有问题

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
            domains = cursor.fetchall()

            # 获取领域项目 最多23个 抛弃项目数为0的领域 domain是tuple类型
            category = {}
            for domain in domains:
                cursor.execute("""
                        select
                            A.pid,
                            A.projection_name,
                            A.projection_image,
                            case when A.publisher_id is null then 'null' else C.user_name end
                        from
                            Project_projectinfo A
                        left join Project_projectimage B on A.pid = B.pid_id
                        left join User_userinfo C on A.publisher_id = C.uid
                        where A.area_id = {}
                        group by A.pid
                        order by count(*) desc
                        limit 23
                    """.format(domain[0]))

                key = ['pid', 'projection_name', 'projection_image', 'user_name']
                category[domain[1]] = [dict(zip(key, item)) for item in cursor.fetchall()]

            cursor.execute("""
                    select 
                        count(*)
                    from 
                        Project_projectinfo
                """)

            project_num = cursor.fetchone()[0]

            cursor.execute("""
                        select 
                            count(*)
                        from 
                            User_userinfo
                    """)

            user_num = cursor.fetchone()[0]

            cursor.execute("""
                        select 
                            count(*)
                        from 
                            Project_domaininfo
                    """)

            domain_num = cursor.fetchone()[0]

            return render(request, 'home.html', {
                'popular_project': projects,
                'category_project': category,
                'project_num': project_num,
                'user_num': user_num,
                'domain_num': domain_num
            })
        if not request.session.get("uid"):
            return render(request, 'User/mobile_preface.html')

        # 获取热门项目
        cursor = connection.cursor()

        cursor.execute("""
            select 
                A.pid,
                A.projection_name,
                date(A.publish_time,'localtime'),
                A.projection_image,
                A.projection_introduction, 
                case when A.publisher_id is null then 'null' else C.user_name end
            from 
                Project_projectinfo A
            left join Project_projectimage B on A.pid = B.pid_id
            left join User_userinfo C on A.publisher_id = C.uid
            group by A.pid
            order by count(*) desc
            limit 10
        """)

        key = ['pid', 'projection_name', 'publish_time', 'projection_image', 'projection_introduction', 'user_name']
        data = {'popular': [dict(zip(key, item)) for item in cursor.fetchall()]}

        return render(request, 'home_mobile.html', data)

    def post(self, request):

        page_cnt = request.POST.get('page_cnt')

        if not page_cnt:
            return JsonResponse({'popular': []})

        cursor = connection.cursor()

        cursor.execute("""
            select 
                A.pid,
                A.projection_name,
                date(A.publish_time,'localtime'),
                A.projection_image,
                A.projection_introduction, 
                case when A.publisher_id is null then 'null' else C.user_name end
            from 
                Project_projectinfo A
            left join Project_projectimage B on A.pid = B.pid_id
            left join User_userinfo C on A.publisher_id = C.uid
            group by A.pid
            order by count(*) desc
            limit {}, 10
        """.format((int(page_cnt) * 10)))

        key = ['pid', 'projection_name', 'publish_time', 'projection_image', 'projection_introduction', 'user_name']
        data = {'popular': [dict(zip(key, item)) for item in cursor.fetchall()]}

        data['total_project'] = ProjectInfo.objects.all().count()

        return JsonResponse(data)


def info(request):
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
    cursor.execute("""
            select  count(*)
            from  User_userinfo
        """)
    all_user = cursor.fetchone()[0]

    cursor.execute("""
            select  count(*)
            from  User_userinfo U
            where  datetime('now','-7 day') < datetime(U.register_date)
        """)
    add_user = cursor.fetchone()[0]

    cursor.execute("""
            select  count(distinct(U.uid))
            from  User_userinfo U join Project_datainfo D on U.uid = D.uid_id 
            where  datetime('now','-7 day') < datetime(D.data_time)
        """)
    active_user = cursor.fetchall()
    active_user = active_user[0][0]
    # print(active_user)
    if all_user == 0:
        add_ratio = "0%"
        active_ratio = "0%"
        add_ratio_int = 0
        active_ratio_int = 0
    else:
        add_ratio = "{}%".format('%.2f' % (add_user / all_user * 100))
        add_ratio_int = int(add_user / all_user * 100)
        active_ratio = "{}%".format('%.2f' % (active_user / all_user * 100))
        active_ratio_int = int(active_user / all_user * 100)

    cursor.execute("""
               select  count(*), A.domain_name
               from  Project_domaininfo A, Project_projectinfo B , Project_projectimage C
               where A.aid = B.area_id and B.pid = C.pid_id
               group by A.aid
               order by count(*) desc
        """)
    result = cursor.fetchall()
    if result != []:
        domain_data = []
        # domain_data_max = result[0][0]
        for domain in result:
            domain_data.append([int(domain[0]), domain[1]])
    else:
        domain_data = []
    # print(domain_data)

    cursor.execute("""
               select  count(*), A.domain_name 
               from  Project_projectinfo B
               left join Project_domaininfo A on A.aid = B.area_id
               group by A.aid
               order by count(*) desc
        """)
    result = cursor.fetchall()
    if result != []:
        domain_project = []
        # domain_project_max = result[0][0]
        for domain in result:
            domain_project.append([int(domain[0]), domain[1]])
    else:
        domain_project = []

    rank_top_k = 5
    domain_data_rank = []
    for domain in domain_data[:rank_top_k]:
        domain_data_rank.append([domain[0], domain[1]])
    # print(domain_data_rank)

    domain_project_rank = []
    for domain in domain_project[:rank_top_k]:
        domain_project_rank.append([domain[0], domain[1]])
    # print(domain_project_rank)

    # 地域分布图
    rank_top_k = 7
    cursor.execute("""
               select  D.data_province, count(*)
               from  Project_domaininfo A, Project_projectinfo B , Project_projectimage C, Project_datainfo D
               where A.aid = B.area_id and B.pid = C.pid_id and C.data_id_id = D.data_id and date('now','-7 day','localtime') < date(D.data_time,'localtime') and D.data_province is not null
               group by D.data_province
               order by count(*) desc
        """)
    result = cursor.fetchall()
    week_data = []
    week_data_graph = []
    week_province_list = []
    for location in result[:rank_top_k]:
        week_data.append([location[0], int(location[1])])
    for location in result:
        week_data_graph.append([location[0], int(location[1])])
        week_province_list.append(location[0])
    for pro in province_list:
        if not pro in week_province_list:
            week_data_graph.append([pro, 0])

    cursor.execute("""
               select  D.data_province, count(*)
               from  Project_domaininfo A, Project_projectinfo B , Project_projectimage C, Project_datainfo D
               where A.aid = B.area_id and B.pid = C.pid_id and C.data_id_id = D.data_id and date('now','-1 month','localtime') < date(D.data_time,'localtime') and D.data_province is not null
               group by D.data_province
               order by count(*) desc
        """)
    result = cursor.fetchall()
    month_data = []
    month_data_graph = []
    month_province_list = []
    for location in result[:rank_top_k]:
        month_data.append([location[0], int(location[1])])
    for location in result:
        month_data_graph.append([location[0], int(location[1])])
        month_province_list.append(location[0])
    for pro in province_list:
        if not pro in month_province_list:
            month_data_graph.append([pro, 0])

    cursor.execute("""
               select  D.data_province, count(*)
               from  Project_domaininfo A, Project_projectinfo B , Project_projectimage C, Project_datainfo D
               where A.aid = B.area_id and B.pid = C.pid_id and C.data_id_id = D.data_id and date('now','-1 year','localtime') < date(D.data_time,'localtime') and D.data_province is not null
               group by D.data_province
               order by count(*) desc
        """)
    result = cursor.fetchall()
    year_data = []
    year_data_graph = []
    year_province_list = []
    for location in result[:rank_top_k]:
        year_data.append([location[0], int(location[1])])
    for location in result:
        year_data_graph.append([location[0], int(location[1])])
        year_province_list.append(location[0])
    for pro in province_list:
        if not pro in year_province_list:
            year_data_graph.append([pro, 0])

    # 折线图
    cursor.execute("""
               select  date(D.data_time), count(*)
               from  Project_datainfo D
               where  date('now','-1 year') < date(D.data_time)
               group by date(D.data_time)
               order by date(D.data_time) asc
        """)
    result = cursor.fetchall()
    website_data = []
    # date_list = []
    year_ago = (datetime.date.today() - datetime.timedelta(days=366))
    for i in range(365):
        year_ago = year_ago + datetime.timedelta(days=1)
        website_data.append([year_ago.strftime("%Y-%m-%d"), 0])

    for data in result:
        for i in range(len(website_data)):
            if website_data[i][0] == data[0]:
                website_data[i][1] = data[1]
        # website_data.append([data[0], data[1]])
        # date_list.append(data[0])

    cursor.execute("""
               select  date(U.publish_time), count(*)
               from  Project_projectinfo U
               where  date('now','-1 year') < date(U.publish_time)
               group by date(U.publish_time)
               order by date(U.publish_time) asc
        """)
    result = cursor.fetchall()
    website_project = []
    year_ago = (datetime.date.today() - datetime.timedelta(days=366))
    for i in range(365):
        year_ago = year_ago + datetime.timedelta(days=1)
        website_project.append([year_ago.strftime("%Y-%m-%d"), 0])
    for data in result:
        for i in range(len(website_project)):
            if website_project[i][0] == data[0]:
                website_project[i][1] = data[1]
    # print(add_ratio, add_ratio)
    # print("week_data:", week_data)
    # print("month_data:", month_data)
    # print("year_data:", year_data)
    # print("website_data:", website_data)
    #
    # print("week_data_graph:", week_data_graph)
    # print("month_data_graph:", month_data_graph)
    # print("year_data_graph:", year_data_graph)
    return render(request, 'website_info.html', {
        'all_user': all_user,  # 总人数
        'add_user': add_user,  # 新增用户个数
        'add_ratio': add_ratio,  # 百分数型字符串
        'add_ratio_int': add_ratio_int,  # 百分数型字符串
        'active_user': active_user,  # 活跃用户数
        'active_ratio': active_ratio,  # 百分数型字符串
        'active_ratio_int': active_ratio_int,  # 百分数型字符串

        # 以下为雷达图所需数据
        # 'domain_data': [[10, 'domain_A'], [30, 'domain_B'], [10, 'domain_A'], [30, 'domain_B'], [10, 'domain_A'],
        #                 [30, 'domain_B'], [30, 'domain_B']],  # 三维列表，分别是数据量，最大值，领域名称
        # 'domain_project': [[1, 'domain_A'], [3, 'domain_B']],  # 要展示的领域的项目量，最大值，领域名称
        # 'year': [['安徽', 2], ['山东', 45]],  # 从日的角度 地域提交量
        # 'week': [['安徽', 233], ['山东', 209388]],  # 从周的角度，……
        # 'month': [['安徽', 452], ['山东', 455]],  # 从月的角度……
        'domain_data': domain_data,  # 三维列表，分别是数据量，最大值，领域名称
        'domain_project': domain_project,  # 要展示的领域的项目量，最大值，领域名称
        'domain_data_rank': domain_data_rank,  # 二维列表，从数据维度看前5的领域数据量
        'domain_project_rank': domain_project_rank,  # 二维列表，从项目角度看前五的领域项目量
        'week': week_data,  # 从周的角度，……
        'month': month_data,  # 从月的角度……
        'year': year_data,  # 从日的角度 地域提交量
        # 以上三个均为二维列表，长度小于8
        # 'website_data': [["1998-06-05", 116], ["1998-06-06", 129], ["1998-06-07", 135]],  # 自网站开始，每天的数据量，二维列表
        'website_data': website_data,  # 自网站开始，每天的数据量，二维列表
        'province_data_week': week_data_graph,
        'max_week': week_data_graph[0][1] if week_data_graph != [] else 0,  # province_data中所有数据最大值，后端处理，加快渲染速度
        'province_data_month': month_data_graph,
        'max_month': month_data_graph[0][1] if month_data_graph != [] else 0,  # province_data中所有数据最大值，后端处理，加快渲染速度
        'province_data_year': year_data_graph,
        'max_year': year_data_graph[0][1] if year_data_graph != [] else 0,  # province_data中所有数据最大值，后端处理，加快渲染速度
        'website_project': website_project
    })
