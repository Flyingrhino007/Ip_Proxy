# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: ProxyValidSchedule.py
Author: JoeyCAO
Time: 2019/1/16 21:52
Description: 从数据库useful_proxy中取出代理，开启多线程逐个验证
--------------------------------------------------
"""
import sys
import time
from queue import Queue

sys.path.append('../')

from Schedule.ProxyCheck import ProxyCheck
from Manager.ProxyManager import ProxyManager


class ProxyValidSchedule(ProxyManager, object):
    def __init__(self):
        ProxyManager.__init__(self)
        self.queue = Queue()
        self.proxy_item = []

    def __validProxy(self, threads=5):
        """
        验证useful_proxy代理
        :param threads:
        :return:
        """
        thread_list = []
        for index in range(threads):
            thread_list.append(ProxyCheck(self.queue, self.proxy_item)) # proxy_item中一开始都为空，调用check函数，对应的proxy检验失败，该位置的num就++，直到超过阈值
        for thread in thread_list:
            thread.daemon = True                                    # daemon 线程存在时主程序不会退出，等待该daemon线程结束，主程序才退出
            thread.start()
        for thread in thread_list:
            thread.join()

    def main(self):
        self.putQueue()                                             # 调用putQueue()
        while True:                                                 # 循环
            if not self.queue.empty():                              # 不空则验证proxy是否有效
                self.log.info('Start valid useful proxy')
                self.__validProxy()
            else:                                                   # 空则验证结束，等待5分钟，再次取出验证
                self.log.info('Valid Complete! sleep 5 minutes.')
                time.sleep(60 * 20)
                self.putQueue()


    def putQueue(self):
        """
        从useful_table取proxy，放入到类的队列中
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.proxy_item = self.db.getAll()
        for item in self.proxy_item:
            self.queue.put(item)


def run():
    p = ProxyValidSchedule()
    p.main()


if __name__ == "__main__":
    p = ProxyValidSchedule()
    p.main()