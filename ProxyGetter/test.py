# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: test.py
Author: Administrator
Time: 2019/1/17 13:05
Description: 111
--------------------------------------------------
"""
from Util.WebRequest import WebRequest

def freeProxyRaw():
    """
    https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt
    :return:
    """
    try:
        txt = open('free-proxy-list.txt')
        contens = txt.readlines()
        ipdict = []
        for line in contens:
            # ipdict.append({'http': line.replace('\n', '')})
            ipdict.append(line.replace('\n', ''))
        txt.close()
        print(ipdict)
    except Exception as e:
        print(r'proxy_list ip_get failed', e)
        return


if __name__ == "__main__":
    freeProxyRaw()