# -*- coding: UTF-8 -*-

#================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：apiTest.py
#   Author：Yong Bai
#   Time：2019-05-19 21:23:31
#   Description：
#
#================================================================
import requests
from os.path import basename,join
from glob import glob
from random import shuffle


class ApiTest:
    def __init__(self,kind):
        self.url = 'http://114.116.29.7/project/submit/type={}/'.format(kind)
        self.true = 0
        self.false = 0
    def test(self,path):
        file = {
                'image':(basename(path),open(path,'rb'))
                }
        #print (file)
        result = requests.post(self.url,files=file).json()
        if result['result']==True:
            self.true += 1
        #print (result)

if __name__=='__main__':
    root ='/mnt/d/baiyong/code/OmniSci/OmniSci/Project/static/project_image/plant'
    imgs = glob(join(root,'*.jpg'))
    shuffle(imgs)
    imgs = imgs[:1000]

    apiHelper = ApiTest('tree')
    for idx,img in enumerate(imgs):
        apiHelper.test(img)
        if idx%50 == 49:
            print (idx,':',(float)(apiHelper.true)/idx)
    print ('Acc:',(float)(apiHelper.true)/len(imgs))
