#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from configparser import ConfigParser
import yaml
from common.Log import log
import configparser
from common.set_title import getrootdirectory

data_file_path = os.path.join(getrootdirectory(), "config", "setting.ini")
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


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


def modify_ini_and_write(section, key, new_value):
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser(allow_no_value=True)

    # 读取 .ini 文件的内容
    with open(data_file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # 将内容传递给 ConfigParser 以保留注释
    config.read_string(''.join(content))
    try:
        # 修改配置值
        if section in config and key in config[section]:
            config.set(section, key, new_value)
        else:
            log.error(f"Error: Key '{key}' in section '{section}' not found in '{file_path}' or section not found.")
        # 保存更改到 .ini 文件
        with open(data_file_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        log.info(f"项目环境：{new_value} 已写入setting.ini配置文件.")
    except Exception as e:
        log.error(f"{e}")
        return False
    else:
        return True


