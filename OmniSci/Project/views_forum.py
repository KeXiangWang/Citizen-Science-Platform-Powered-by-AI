import os
import math

from .models import *
from User.models import UserInfo

from django.db import connection
from django.http import JsonResponse

from Project.utils.trans_str import transform

base_dir = os.path.dirname(os.path.abspath(__file__))


def forum(request, issue_id):
    """ 获讨论区页面所需数据

    Args:
        request

        issue_id

    Returns:
        返回数据搜索页面需要的数据(JSON格式)，例如：
        {
            'comment_page_cnt': ...
            'issue':
                {
                    'issue_id': ...
                    'title': ...
                    'description': ...
                    'time':  ...
                    'user_name': ...
                }
        }
    """
    data = {}
    cursor = connection.cursor()
    cursor.execute("""
        select
            count(*)
        from
            Project_commentinfo A
        where A.issue_id_id = {}
    """.format(issue_id))

    data['comment_page_cnt'] = math.ceil(cursor.fetchone()[0] / 5)

    cursor.execute("""
            select 
                A.issue_id,
                A.title,
                A.description,
                date(A.time,'localtime'),
                case when A.uid_id is null then 'null' else B.user_name end
            from 
                Project_issueinfo A
            left join User_userinfo B on A.uid_id = B.uid
            where A.issue_id = {}
        """.format(issue_id))

    key = ['issue_id', 'title', 'description', 'time', 'user_name']
    data['issue'] = dict(zip(key, cursor.fetchone()))
    return JsonResponse(data)


def forum_page(request, pid, page_num):
    """ 获取post数据（一页）

    Args:
        request

        pid

        page_num

    Returns:
        返回讨论区页面需要的数据(JSON格式)，例如：
        [
            {
                'issue_id': ...
                'title': ...
                'description': ...
                'time':  ...
                'user_name': ...
            }
        ]
    """
    cursor = connection.cursor()
    cursor.execute("""
        select
            A.issue_id,
            A.title,
            A.description,
            date(A.time,'localtime'),
            case when A.uid_id is null then 'null' else C.user_name end
        from
            Project_issueinfo A,
            Project_projectissue B
        left join User_userinfo C on A.uid_id = C.uid
        where B.pid_id = {} and B.issue_id_id = A.issue_id
        limit {}, 5
    """.format(pid, (page_num - 1) * 5))

    key = ['issue_id', 'title', 'description', 'time', 'user_name']
    data = {'issue': [dict(zip(key, item)) for item in cursor.fetchall()]}

    return JsonResponse(data)


def comment_page(request, issue_id, page_num):
    """ 获取comment数据（一页）

    Args:
        request

        issue_id

        page_num

    Returns:
        返回讨论区帖子详情页面需要的数据(JSON格式)，例如：
        [
            {
                'text': ...
                'time': ...
                'user_name': ...
            }
        ]
    """
    cursor = connection.cursor()
    cursor.execute("""
        select
            A.text,
            date(A.time, 'localtime'),
            case when A.uid_id is null then 'null' else B.user_name end
        from
            Project_commentinfo A
        left join User_userinfo B on A.uid_id = B.uid
        where A.issue_id_id = {}
        order by A.time
        limit {}, 5
    """.format(issue_id, (page_num - 1) * 5))

    key = ['text', 'time', 'user_name']
    data = {'comment': [dict(zip(key, item)) for item in cursor.fetchall()]}

    return JsonResponse(data)


def response(request, pid, issue_id):
    """ 处理用户issue回复

    判断用户信息，用户权限等，修改数据库

    Args:
        request

        pid

        issue_id

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
    issue = IssueInfo.objects.filter(issue_id=issue_id)[0]

    # 判断用户对于项目的权限
    if len(authorities) == 0:
        msg['msg'] = 'Please participate project firstly'
        return JsonResponse(msg)

    # 判断填写情况
    content = request.POST.get('content')
    preview = request.POST.get('preview')
    line = request.POST.get('line')
    if not content or len(content) <= 0 or not preview or len(preview) <= 0 or not line:
        msg['msg'] = 'Please fill in the response'
        return JsonResponse(msg)

    try:
        if (len(preview) - int(line) * 2) > 100:
            msg['msg'] = 'Too long response'
            return JsonResponse(msg)
    except:
        msg['msg'] = 'Wrong'
        return JsonResponse(msg)

    # 存储评论
    CommentInfo(
        issue_id=issue,
        uid=user,
        text=content
    ).save()

    cursor = connection.cursor()
    cursor.execute("""
        select
            count(*)
        from
            Project_commentinfo A
        where A.issue_id_id = {}
    """.format(issue_id))

    msg['comment_page_cnt'] = math.ceil(cursor.fetchone()[0] / 5)

    msg['result'] = True
    msg['msg'] = 'Response successfully'

    return JsonResponse(msg)


def add_post(request, pid):
    """ 处理issue增加

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

    # 判断用户对于项目的权限
    if len(authorities) == 0:
        msg['msg'] = 'Please participate project firstly'
        return JsonResponse(msg)

    # 判断填写情况
    title = request.POST.get('title')
    description = request.POST.get('description')
    if not title or len(title) <= 0 or \
            not description or len(description) <= 0:
        msg['msg'] = 'Please fill in the content'
        return JsonResponse(msg)

    if len(title) > 100 or len(description) > 280:
        msg['msg'] = 'Too long content'
        return JsonResponse(msg)

    # 存储issue
    IssueInfo(
        uid=user,
        title=transform(title),
        description=transform(description)
    ).save()

    # 存储issue project关系
    ProjectIssue(
        pid=project,
        issue_id=IssueInfo.objects.last()
    ).save()

    msg['result'] = True
    msg['msg'] = 'Add post successfully'

    return JsonResponse(msg)
