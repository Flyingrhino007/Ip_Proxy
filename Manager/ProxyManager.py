# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py
   Description :  代理控制器，负责从免费网站抓取Ip刷新库，负责调用数据库接口返回，查询，修改，删除数据
   Author :       JoeyCAO
   date：          2019/1/6
-------------------------------------------------
   Change Activity:
                   2019/1/16:
-------------------------------------------------
"""
__author__ = 'JoeyCAO'

import random
from Util.LogHandler import LogHandler
from DB.DbClient import DbClient
from Util.GetConfig import config
from ProxyGetter.getFreeProxy import GetFreeProxy
from ProxyGetter.CheckProxy import verifyProxyFormat


class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self):
        self.db = DbClient()
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def get(self):
        """
        return a useful proxy
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if item_dict:
            return random.choice(list(item_dict.keys()))
        return None
        # return self.db.pop()

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool as list
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        return list(item_dict.keys()) if item_dict else list()

    def getNumber(self):
        self.db.changeTable(self.raw_proxy_queue)
        total_raw_proxy = self.db.getNumber()
        self.db.changeTable(self.useful_proxy_queue)
        total_useful_queue = self.db.getNumber()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}

    def refresh(self):
        """
        通过ProxyGetter/getFreeProxy取代理并放入数据库
        :return:
        """
        self.db.changeTable(self.raw_proxy_queue)               # 切换到生肉列表
        for proxyGetter in config.proxy_getter_functions:
            # 开始按照config.ini中指定的抓取函数逐个运行
            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                for proxy in getattr(GetFreeProxy, proxyGetter.strip())():  # getattr后面加()，直接运行该函数，即运行某个抓取函数
                    #
                    proxy = proxy.strip()
                    if proxy and verifyProxyFormat(proxy):                  # 验证proxy符合IP代理的格式
                        self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                        self.db.put(proxy)                                  # 验证通过加入数据库
                    else:
                        self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))   # 验证出错记录bug
            except Exception as e:
                self.log.error("{func}: fetch proxy fail".format(func=proxyGetter))
                continue



if __name__ == '__main__':
    pp = ProxyManager()