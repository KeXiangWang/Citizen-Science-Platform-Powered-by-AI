# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：createProjects.py
#   Author：Yong Bai
#   Time：2019-04-09 18:41:39
#   Description：
#
# ================================================================


from django.core.management.base import BaseCommand, CommandError
from Project.utils.addProject import addProjects, addIssue, addImage, addUser, addUserProjectAuthority

class Command(BaseCommand):
    help = '批量生成项目数据'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        addUser()
        addProjects()
        addUserProjectAuthority()
        addImage()
        # addIssue()
        self.stdout.write('Successfully Add Projects And Users')
        # try:
        #     addProjects()
        #     self.stdout.write('Successfully Add Projects')
        # except:
        #     raise CommandError('Something Wrong')
