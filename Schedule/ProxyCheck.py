# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: ProxyCheck.py
Author: JoeyCAO
Time: 2019/1/16 21:24
Description: 从给定的queue中验证采集到的proxy，每隔proxy有可以验证Fail_count次数，验证通过就加入数据库useful_table
--------------------------------------------------
"""

import sys
from threading import Thread

sys.path.append('../')

from Util.utilFunction import validUsefulProxy
from Manager.ProxyManager import ProxyManager
from Util.LogHandler import LogHandler

FAIL_COUNT = 1 # 检验失败次数，超过即删除代理


class ProxyCheck(ProxyManager, Thread):
    def __init__(self, queue, item_dict):
        ProxyManager.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check', file=False)    # 多线程同时写一个日志文件会有问题？？？？
        self.queue = queue                                  # 创建线程时传入已经搜集到的proxy队列
        self.item_dict = item_dict

    def run(self):
        self.db.changeTable(self.useful_proxy_queue)
        while self.queue.qsize():                           # 队列不为空即进入循环
            proxy = self.queue.get()                        # 从队列中取出proxy
            count = self.item_dict[proxy]                   #
            if validUsefulProxy(proxy):
                # 验证通过即计数器减1
                if count and int(count) > 0:
                    self.db.put(proxy, num=int(count) - 1)
                else:
                    pass
                self.log.info('ProxyCheck: {} validation pass'.format(proxy))
            else:
                self.log.info('ProxyCheck: {} validation fail'.format(proxy))
                if count and int(count) + 1>= FAIL_COUNT:   # 用FAIL_COUNT 控制计数的次数，如果检验失败num就+1，直到大于FAIL_COUNT就从队列中删除
                    self.log.info('ProxyCheck: {} fail too many, delete!'.format(proxy))
                    self.db.delete(proxy)
                else:
                    self.db.put(proxy, num=int(count) + 1)
            self.queue.task_done()


if __name__ == "__main__":
    pass
