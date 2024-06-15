#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from configparser import ConfigParser
import yaml
from common.Log import log

class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#读取yaml文件
def read_yaml_token():
    with open(BASE_PATH +'/extract_token.yaml',encoding="utf-8") as f:
        value = yaml.load(stream=f,Loader=yaml.FullLoader)
        log.info("读到token ==>>  {}".format(value))
        return value

def read_yamlcase(yamlcase_name):
    log.info("加载 ==>> {}文件.....".format(yamlcase_name))
    with open(yamlcase_name,encoding="utf-8") as f:
        value = yaml.load(stream=f,Loader=yaml.FullLoader)
        log.info("读到数据 ==>>  {}".format(value))
        return value
# 写入yaml文件，,mode='a'表示追加的方式写入
# def write_yaml(data):
#     with open(os.getcwd()+'/extract_token.yml',encoding="utf-8",mode='a') as f:
#         yaml.dump(data,stream=f,allow_unicode=True)

def write_yaml(data,yaml_file):
    log.info("获取token：{}......".format(data))
    with open(os.getcwd()+yaml_file,encoding="utf-8",mode="a") as f:
        yaml.dump(data,stream=f,allow_unicode=True)
        log.info("已将{}写入{}文件......".format(data,yaml_file))

#清空yaml文件，mode='w'写入
def clear_yaml(yaml_file):
    with open(os.getcwd()+yaml_file,encoding="utf-8",mode='w') as f:
        f.truncate()
        log.info("重置 {}文件.......".format(yaml_file))

def load_ini(file_path):
    log.info("加载 {} 文件......".format(file_path))
    config = MyConfigParser()
    config.read(file_path, encoding="UTF-8")
    data = dict(config._sections)
    return data
