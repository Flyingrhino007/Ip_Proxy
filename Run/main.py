# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: main.py
Author: JoeyCAO
Time: 2019/1/16 19:30
Description: 111
--------------------------------------------------
"""
import sys
from multiprocessing import Process

sys.path.append('.')
sys.path.append('..')

from Api.ProxyApi import run as ApiRun
from Schedule.ProxyRefreshSchedule import run as RefreshRun
from Schedule.ProxyValidSchedule import run as ValidRun


def run():
    p_list = []
    p1 = Process(target=ApiRun, name="ApiRun")
    p2 = Process(target=RefreshRun, name="RefreshRun")
    p3 = Process(target=ValidRun, name="ValidRun")
    p_list.append(p1)
    p_list.append(p2)
    p_list.append(p3)

    for p in p_list:
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()

if __name__ == "__main__":
    run()
