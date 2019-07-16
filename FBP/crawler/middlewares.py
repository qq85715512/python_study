# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
import os
from crawler.settings import USER_AGENT_LIST


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        rand_use = random.choice(USER_AGENT_LIST)
        if rand_use:
            request.headers.setdefault('User-Agent', rand_use)


class ProxySpiderMiddleware(object):
    """docstring for ProxyMiddleWare"""
    def process_request(self,request, spider):
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        print("this is request ip:"+proxy)
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip:"+proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy
            return request
        return response

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        path1=os.path.abspath('.')   #表示当前所处的文件夹的绝对路径
        while 1:
            with open(path1+'\\crawler\\proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                # time.sleep(1)
                pass
        proxy = random.choice(proxies).strip()
        return proxy