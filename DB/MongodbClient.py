# -*- coding: utf-8 -*-
"""
--------------------------------------------------
Project: Ip_proxy_pool
File name: MongodbClient.py
Author: Administrator
Time: 2019/1/17 10:14
Description: 111
--------------------------------------------------
"""

from pymongo import MongoClient


class MongodbClient(object):
    def __init__(self, name, host, port, **kwargs):
        self.name = name
        self.client = MongoClient(host, port, **kwargs)
        self.db = self.client.proxy

    def changeTable(self, name):
        self.name = name

    def get(self, proxy):
        data = self.db[self.name].find_one({'proxy': proxy})
        return data['num'] if data != None else None

    def put(self, proxy, num=1):
        if self.db[self.name].find_one({'proxy': proxy}):
            return None
        else:
            self.db[self.name].insert({'proxy': proxy, 'num': num})

    def pop(self):
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            value = data['proxy']
            self.delete(value)
            return {'proxy': value, 'value': data['num']}
        return None

    def delete(self, value):
        self.db[self.name].remove({'proxy': value})

    def getAll(self):
        return {p['proxy']: p['num'] for p in self.db[self.name].find()}

    def clean(self):
        self.client.drop_database('proxy')

    def delete_all(self):
        self.db[self.name].remove()

    def update(self, key, value):
        self.db[self.name].update({'proxy': key}, {'$inc': {'num': value}})

    def exists(self, key):
        return True if self.db[self.name].find_one({'proxy': key}) != None else False

    def getNumber(self):
        return self.db[self.name].count()


if __name__ == "__main__":
    db = MongodbClient('raw_proxy', 'localhost', 27017)
    # db.put('127.0.0.1:1')
    # db2 = MongodbClient('second', 'localhost', 27017)
    # db2.put('127.0.0.1:2')
    db.put('http://230.32.62.1:80')
    db.put('http://230.32.622.1:80')
    db.put('http://230.321.622.1:80')
    # print(db.update('http://230.32.622.1:80', 1))

    # print(db.pop())