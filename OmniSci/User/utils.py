# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：utils.py
#   Author：Yong Bai
#   Time：2019-04-13 11:07:03
#   Description：
#
# ================================================================

from uuid import uuid1
from os.path import join
import requests

class FileHelper:
    # request.FILES 图片的读取和储存
    def __init__(self, file, file_key='image'):
        self.img = file.get(file_key)

    def write(self, path, prefix='/static\\images\\avatar',default_image='avatar.png'):
        # 没有上传图片，使用默认头像
        if not self.img:
            return join(prefix,default_image)
        else:
            name = '{}.png'.format(uuid1())
            # 前端 canvas 存图片时存为png
            with open(join(path, name), 'wb+') as f:
                for chunk in self.img.chunks():
                    f.write(chunk)

            return join(prefix,name)


def is_pc(agent):
    agent = agent.lower()
    keywords = ["mobile","android","iphone","ipad","phone"]
    for item in keywords:
        if item in agent:
            return False
    return True


def make_sense(something):
    return  (something!=None and something!='' and something!='undefined')
