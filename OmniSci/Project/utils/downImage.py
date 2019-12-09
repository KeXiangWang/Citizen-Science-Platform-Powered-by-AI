# -*- coding: UTF-8 -*-

#================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：downImage.py
#   Author：Yong Bai
#   Time：2019-04-10 08:15:29
#   Description：
#
#================================================================

import argparse
from os.path import join
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='list/imgList00')
parser.add_argument('--output', default='img')

opts = parser.parse_args()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

with open(opts.input,'r') as f:
    line = f.readline()
    while line:
        info = line.split('\t')
        name = info[0].strip()
        url = info[1].strip()
        jpg = requests.get(url, headers=headers)
        file = open(join(opts.output,name), 'wb')
        file.write(jpg.content)
        file.close()
        print ('finish:\t',name)
        line = f.readline()

