# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: utilFunction.py
Author: JoeyCAO
Time: 2019/1/16 19:32
Description: JoeyCAO
--------------------------------------------------
"""
import requests
import time
from lxml import etree

from Util.LogHandler import LogHandler
from Util.WebRequest import WebRequest


def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass

    return decorate


def verifyProxyFormat(proxy):
    """
    检查代理格式是否正确
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    # 若匹配成功，且只匹配了1个，就返回True
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    wr = WebRequest()

    time.sleep(2)

    html = wr.get(url=url, header=header).content
    return etree.HTML(html)


def tcpConnect(proxy):
    """
    TCP三次握手连接，测试TCP连接是否有效
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    # 用 socket（）函数来创建套接字
    s = socket(AF_INET, SOCK_STREAM)        # IPV4 + TCP连接
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))      # connect()函数的扩展版本,出错时返回出错码,而不是抛出异常
    return True if result == 0 else False


def validUsefulProxy(proxy):
    """
    检验代理是否可用,http://httpbin.org/ip为测试网站，返回本地ip地址
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf-8')
    proxies = {'http': "http://{proxy}".format(proxy=proxy)}
    try:
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            return True
    except Exception as e:
        return False