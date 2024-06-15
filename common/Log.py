#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import logging
import os
import time

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 定义日志文件路径
LOG_PATH = os.path.join(BASE_PATH, "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

class Log:

    def __init__(self,level='DEBUG',name=__name__):
        self.logname = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y%m%d")))
        self.log =logging.getLogger(name)
        self.log.handlers.clear()
        self.log.setLevel(level)

    def handler(self,level='DEBUG'):
        handler = logging.FileHandler(self.logname,mode='a', encoding='utf-8')
        handler.setLevel(level)
        handler.setFormatter(self.get_formatter())
        return handler

    def stream_handler(self,level='DEBUG'):
        handler_stream = logging.StreamHandler()
        handler_stream.setLevel(level)
        handler_stream.setFormatter(self.get_formatter())
        return handler_stream

    def get_formatter(self):
        formatter = logging.Formatter('[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')
        # formatter = logging.Formatter('[%(asctime)s] -->> %(name)s >> %(levelname)s - %(message)s')
        # formatter_str = logging.Formatter('%(asctime)s -->> %(filename)s %(lineno)d-->> %(levelname)s - %(message)s',datefmt='%Y/%m/%d %H:%M:%S')
        return formatter

    def get_log(self):
        self.log.addHandler(self.stream_handler())
        self.log.addHandler(self.handler())
        return self.log

log = Log().get_log()
if __name__ == '__main__':
    # log = Log(name='test_11111').get_log()
    # log.info("test")
    # log.info("test111")
    # log.info("test222")
    # log.info("test333")

    log.info('test')