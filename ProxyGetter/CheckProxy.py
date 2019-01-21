# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: CheckProxy.py
Author: JoeyCAO
Time: 2019/1/16 20:46
Description: 测试proxy是否有用
--------------------------------------------------
"""
import sys
from ProxyGetter.getFreeProxy import GetFreeProxy
from Util.utilFunction import verifyProxyFormat

sys.path.append('../')

from Util.LogHandler import LogHandler

log = LogHandler('check_proxy', file=False)


class CheckProxy(object):

    @staticmethod
    def checkAllGetProxyFunc():
        """
        检查所有GetFreeProxy函数运行情况
        :return:
        """
        # inspect.getmembers返回值为object的所有成员，以（name,value）对组成的列表
        import inspect
        member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)
        proxy_count_dict = []
        for func_name, func in member_list:
            log.info(u"开始运行 {}".format(func_name))
            try:
                proxy_list = [ p for p in func() if verifyProxyFormat(p)]   # 每个免费代理获取函数产生N个proxy，测试其格式是否正确，正确即加入list
                proxy_count_dict[func_name] = len(proxy_list)                # 获取了多少个proxy，列表就有多长
            except Exception as e:
                log.info(u"代理获取函数 {} 运行出错".format(func_name))
                log.error(str(e))
        log.info(u"所有函数运行完毕 " + "***" * 5)
        for func_name, func in member_list:
            log.info(u"函数 {n}, 获取到代理数: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))

    @staticmethod
    def checkGetProxyFunc(func):
        """
        检查指定的GetFreeProxy单个函数的运行情况
        :param func:
        :return:
        """
        func_name = getattr(func, '__name__', "None")
        log.info("start running func: {}".format(func_name))
        count = 0
        for proxy in func():
            if verifyProxyFormat(proxy):
                log.info("{} fetch proxy: {}".format(func_name, proxy))
                count += 1
        log.info("{n} completed, fetch proxy number: {c}".format(n=func_name, c=count))


if __name__ == "__main__":
    CheckProxy.checkAllGetProxyFunc()
    CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyFirst)