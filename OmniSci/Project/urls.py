"""OmniSci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from django.conf.urls import url

from . import views, views_detail, views_domain, views_forum, views_manage, views_ai

urlpatterns = [

    # Release
    path(r'release/', views.Release.as_view(), name='Release'),

    # Detail
    path(r'detail/<int:pid>/', views_detail.Detail.as_view(), name='Detail'),
    path(r'detail_page/<int:pid>/<int:page_num>/<int:verified>/', views_detail.Detail.as_view(), name='DetailPage'),
    path(r'detail_page_cnt/<int:pid>/<int:verified>/', views_detail.get_page_cnt, name='PageCnt'),
    path(r'join/<int:pid>/', views_detail.user_join, name='Join'),
    path(r'submit/<int:pid>/', views_detail.user_submit, name='Submit'),
    path(r'bad_submit/', views_detail.bad_submit, name='WrongSubmit'),
    path(r'audition/<int:pid>/', views_detail.user_audition, name='Audition'),
    path(r'audition_all/<int:pid>/', views_detail.user_audition_all, name='Audition'),

    # AI
    path(r'submit/type=animal/', views_ai.judge_animal, name="JudgeAnimal"),
    path(r'submit/type=fruit/', views_ai.judge_fruit, name="JudgeFruit"),
    path(r'submit/type=tree/', views_ai.judge_tree, name="JudgeTree"),

    # Manage
    path(r'download/<int:pid>', views_manage.download, name='Download'),
    path(r'update/', views_manage.update, name='Update'),
    path(r'updateModel/', views_manage.updateModel, name='UpdateModel'),
    path(r'delete/', views_manage.delete, name='Delete'),
    path(r'addAuthority/<int:pid>/', views_manage.add_authority, name='AddAuthority'),
    path(r'removeAuthority/<int:pid>/', views_manage.remove_authority, name='RemoveAuthority'),


    # Forum
    path(r'forum/<int:issue_id>/', views_forum.forum, name='Forum'),
    path(r'forum_page/<int:pid>/<int:page_num>/', views_forum.forum_page, name='ForumPage'),
    path(r'comment_page/<int:issue_id>/<int:page_num>/', views_forum.comment_page, name='CommentPage'),
    path(r'response/<int:pid>/<int:issue_id>/', views_forum.response, name='Response'),
    path(r'addPost/<int:pid>/', views_forum.add_post, name='AddPost'),

    # Domain
    path(r'domain/<str:domain_name>/', views_domain.Domain.as_view(), name='Domain'),
    path(r'search/', views.search, name='Search'),


    # Mobile
    path(r'm_project/<int:pid>', views.mobile, name='MobileProject'),

    # debug
    path(r'm_domain/debug', views.m_category_debug, name='MobileCategoryDebug'),
    path(r'm_info', views.m_info_debug, name='MobileInfoDebug'),
    path(r'detail/debug', views.detail_debug,name='DetailDebug'),
]
