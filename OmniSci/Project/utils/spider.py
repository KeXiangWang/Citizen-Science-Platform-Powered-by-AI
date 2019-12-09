# 10:33 AM, Feb 21th, 2018 @ home, Shangyu
# Pexels Crawler
# 按照关键字爬取 Pexels 网站的图片
# https://www.pexels.com/
# pexels 网站的异步加载比较容易破解
# 在关键词后面加page即可
# 如
# https://www.pexels.com/search/fun/?page=4
# https://www.pexels.com/search/fun/?page=5


import os
import time
import requests
from bs4 import BeautifulSoup
from os.path import exists,join
import json as js

class Spider:

    def __init__(self,dir,num):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.alljpg_srcs = []
        self.dir = dir
        self.total = num
        self.realDownload = False

        if not exists(dir):
            os.makedirs(dir)
        if not self.realDownload:
            self.listFile = open(join(dir,'imgList.txt'),'a+')

    def download(self,keyword):
        keyword = keyword.strip()  # 除去首尾空格
        count = 0
        path = join(self.dir,keyword)
        # 创建文件夹
        if not exists(path):
            os.makedirs(path)

        for page in range(1,10):
            url = 'https://www.pexels.com/search/{keyword}/?page={page}'.format(keyword=keyword,page=page)
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'lxml')
            jpg_srcs = soup.select('body > div.page-wrap > div.l-container > div.photos > div.photos__column > div.hide-featured-badge > article > a > img.photo-item__img')
            # print(jpg_srcs)
            for item in jpg_srcs:
                self.alljpg_srcs.append(item)
                jpg_src = item.get('src')
                print(count,jpg_src)
                imgName =  '{}_{}.jpg'.format(keyword, count)
                if self.realDownload:
                    jpg = requests.get(jpg_src, headers=self.headers)
                    file = open(join(path,imgName), 'wb')
                    file.write(jpg.content)
                    file.close()
                else:
                    self.listFile.write('{}\t{}\n'.format(imgName,jpg_src))
                    self.listFile.flush()
                count += 1
                if count >= self.total:
                    print("Finish")
                    return

            time.sleep(1)


if __name__ == '__main__':
    with open('data.json','r') as f:
        data = js.load(f)

    flag = False
    spiderHelper = Spider(join(os.getcwd(), 'img'), 3)
    for domain,items in data.items():
        for chName,enName in items.items():
            keyword = enName.lstrip("The ").lstrip("A ")
            if keyword=='rain tree':
                flag = True
            if flag:
                try:
                    spiderHelper.download(keyword)
                except BaseException:
                    continue
