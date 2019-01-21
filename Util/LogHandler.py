# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: LogHandler.py
Author: JoeyCAO
Time: 2019/1/16 19:32
Description: 日志文件
--------------------------------------------------
"""
import os

import logging

from logging.handlers import TimedRotatingFileHandler

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')


class LogHandler(logging.Logger):
    """
    LogHandler
    """

    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        else:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        :param level:
        :return:
        """
        file_name = os.path.join(LOG_PATH,'{name}.log'.format(name=self.name))          # os.path.join ，将多个路径组合后返回，注意：第一个绝对路径之前的参数将会被忽略
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1,  backupCount=15)  # 日志回滚，D+interval为每天保存1个，最多15个
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)                       # level输入为None的时候，默认为DEBUG
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)    # 输出格式设置，日期，文件名，行数，level，信息
        self.file_handler = file_handler
        self.addHandler(self.file_handler)

    def __setStreamHandler__(self, level=None):
        """
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)

        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def resetName(self, name):
        """
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()


if __name__ == '__main__':
    log = LogHandler('log_by_joey')
    log.info('test log')
