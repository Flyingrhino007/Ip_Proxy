# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: ProxyRefreshSchedule.py
Author: JoeyCAO
Time: 2019/1/16 22:10
Description: 每隔十分钟从免费网址抓取一次IP，每分钟检查一次raw_queue队列中可用的proxy加入到useful_queue
--------------------------------------------------
"""

import sys
import time
import logging
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from Manager.ProxyManager import ProxyManager
from Util.LogHandler import LogHandler
from Util.utilFunction import validUsefulProxy


sys.path.append('../')      # 将该路径添加到系统的环境变量

logging.basicConfig()


class ProxyRefreshSchedule(ProxyManager):
    """
    定时刷新代理，将raw_queue中的每一个都验证一下，成功的加入useful_queueu
    """
    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('refresh_schedule')

    def validProxy(self):
        """
        验证Raw_proxy_queue中的代理，将有效的放入useful_proxy_queue
        :return:
        """
        self.db.changeTable(self.raw_proxy_queue)
        raw_proxy_item = self.db.pop()
        self.log.info('ProxyRefreshSchedule: %s start validProxy' % time.ctime())
        # 计算剩余代理，用来减少重复计算
        remaining_proxies = self.getAll()
        while raw_proxy_item:                           # 若raw_queue中能弹出item，就继续
            raw_proxy = raw_proxy_item.get('proxy')
            if isinstance(raw_proxy, bytes):
                raw_proxy = raw_proxy.decode('utf-8')
                # 如果raw_proxy不在已经成功的db中，且有效，就将他加入useful_queue
            if (raw_proxy not in remaining_proxies) and validUsefulProxy(raw_proxy):
                self.db.changeTable(self.useful_proxy_queue)
                self.db.put(raw_proxy)
                self.log.info('ProxyRefreshSchedule: %s validation pass' % raw_proxy)
            else:
                self.log.info('ProxyRefreshSchedule: %s validation fail' % raw_proxy)
            self.db.changeTable(self.raw_proxy_queue)           # 切换回raw_queue
            raw_proxy_item = self.db.pop()                      # 弹出raw_queue中的item
            remaining_proxies = self.getAll()                   # 可能加入了新的可用proxy，此处要重新请求，刷新该列表
        self.log.info('ProxyRefreshSchedule: %s validation complete' % time.ctime())


def refreshPool():
    pp = ProxyRefreshSchedule()
    pp.validProxy()


def batchRefresh(process_num=5):
    """
    检验新代理
    :param process_num:
    :return:
    """
    p1 = []
    for num in range(process_num):
        proc = Thread(target=refreshPool, args=())
        p1.append(proc)
    for num in range(process_num):
        p1[num].daemon = True
        p1[num].start()
    for num in range(process_num):
        p1[num].join()


def fetchAll():
    p = ProxyRefreshSchedule()
    # 获取新代理，调用ProxyManager.refresh获取新的代理
    p.refresh()


def run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchAll, 'interval', minutes=180, id="fetch_proxy")   # 调用ProxyManager.refresh获取新的代理，频率太高会增大验证的压力，导致raw_queue积压

    scheduler.add_job(batchRefresh, "interval", minutes=60)                  # 每分钟检查一次新的代理
    scheduler.start()

    fetchAll()                                                              # 马上先执行一次

    while True:
        time.sleep(3)


if __name__ == "__main__":
    run()