# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: DbClient.py
Author: Administrator
Time: 2019/1/17 10:14
Description: 111
--------------------------------------------------
"""

import os
import sys
from DB.MongodbClient import MongodbClient


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DbClient(object):
    """
    DbClient DB工厂类 提供get/put/pop/delete/getAll/changeTable方法
    目前存放代理的table/collection/hash有两种：
        raw_proxy： 存放原始的代理；
        useful_proxy_queue： 存放检验后的代理；
    抽象方法定义：
        get(proxy): 返回proxy的信息；
        put(proxy): 存入一个代理；
        pop(): 弹出一个代理
        exists(proxy)： 判断代理是否存在
        getNumber(raw_proxy): 返回代理总数（一个计数器）；
        update(proxy, num): 修改代理属性计数器的值;
        delete(proxy): 删除指定代理；
        getAll(): 返回所有代理；
        changeTable(name): 切换 table or collection or hash;
        所有方法需要相应类去具体实现：
            SSDB：SsdbClient.py
            REDIS:RedisClient.py  停用 统一使用SsdbClient.py
    """

    # __metaclass__ = Singleton

    def __init__(self):
        """
        init
        :return:
        """
        self.__initDbClient()

    def __initDbClient(self):
        """
        init DB Client
        :return:
        """
        __type = "MongodbClient"
        self.client = MongodbClient('second', 'localhost', 27017)

    def get(self, key):
        return self.client.get(key)

    def put(self, key, **kwargs):
        # key = str(key, encoding="utf-8")
        return self.client.put(key, **kwargs)

    def update(self, key, value, **kwargs):
        return self.client.update(key, value)

    def delete(self, key, **kwargs):
        return self.client.delete(key)

    def exists(self, key, **kwargs):
        return self.client.exists(key)

    def pop(self, **kwargs):
        return self.client.pop()

    def getAll(self):
        return self.client.getAll()

    def changeTable(self, name):
        self.client.changeTable(name)

    def getNumber(self):
        return self.client.getNumber()


if __name__ == "__main__":
    account = DbClient()
    account.changeTable('useful_proxy')
    print(account.pop())