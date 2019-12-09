# -*- coding: UTF-8 -*-

# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：translate.py
#   Author：Yong Bai
#   Time：2019-04-09 21:38:39
#   Description：
#
# ================================================================
import uuid
import requests
import hashlib
import time

# 调用有道的翻译api,可以将输入的中文翻译为英文呢
# 目前用于利用中文关键词爬取pexels上照片
# 不知道以后有啥用，可能可以用于将网站的中文项目描述翻译成英文显示双语?

class Translate:
    def __init__(self):
        self.APP_KEY = '56626e5001cb6a9e'
        self.APP_SECRET = 'VBH9UYguXeM1SGHen46CqOTXZ3klTCGT'
        self.YOUDAO_URL = 'http://openapi.youdao.com/api'
        self.from_language = 'zh-CHS'
        self.to_language = 'en'

    def encrypt(self,signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self,q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self,data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def connect(self,query):
        q = query

        data = {}
        data['from'] = self.from_language
        data['to'] = self.to_language
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign

        response = self.do_request(data)
        result = response.json()
        if result['errorCode']!='0':
            return False, ''
        else:
            return True,result['translation']


# if __name__ == '__main__':
#     transHelper = Translate(u'老虎')
#     transHelper.connect()

