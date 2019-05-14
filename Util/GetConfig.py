# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: GetConfig.py
Author: Administrator
Time: 2019/1/17 10:21
Description: 111
--------------------------------------------------
"""
import os
from Util.utilClass import ConfigParse
from Util.utilClass import LazyProperty


class GetConfig(object):
    """
    get config from Config.ini
    """

    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]         # split返回文件的路径和文件名, realpath获取当前执行脚本的绝对路径。
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'Config.ini')   # 获取Config.ini文件的路径
        # print(self.config_path)
        self.config_file = ConfigParse(defaults={"password": None})
        self.config_file.read(self.config_path)

    @LazyProperty
    def proxy_getter_functions(self):
        return self.config_file.options('ProxyGetter')


config = GetConfig()


if __name__ == "__main__":
    gg = GetConfig()
    print(gg.proxy_getter_functions)
