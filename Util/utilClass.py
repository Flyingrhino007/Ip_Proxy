# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: utilClass.py
Author: Administrator
Time: 2019/1/17 10:51
Description: 111
--------------------------------------------------
"""
from configparser import ConfigParser   # 限py3


class ConfigParse(ConfigParser):
    """
    重写ConfigParser，支持optionstr
    """
    def __init__(self, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)

    def optionxform(self, optionstr):
        # if optionstr:
        #     print(optionstr)
        # else:
        #     # print("buuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuug")
        return optionstr


class Singleton(type):
    pass


class LazyProperty(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)    # 给对象的属性func.__name__,赋值value，若属性不存在，先创建再赋值。
            return value
