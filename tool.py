#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import yaml


def open_json():

    with open('static/data1.json','r',encoding = 'utf-8') as f:
        data = json.load(f)
    print(data)


def write_yaml():
    # 要写入文件的数据
    data = """
        "test_01:"
        [["登录", "错误登录", "post", "/api/typhon/passport/exchange/pass-token/by-password"]]"""
    # module, name, method, url, data,except_pt,except_code,except_result
    # 模块名称，用例名称，请求方式，链接，数据，成功断言，状态码断言，内容是否存在断言，非空断言不需要填写

    # 写入YAML文件
    with open('output.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

write_yaml()