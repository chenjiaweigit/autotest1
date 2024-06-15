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
    # data = """
    #     "test_01:"
    #     [["登录", "错误登录", "post", "/api/typhon/login"]]"""
    data = ["test_01",
            ["登录", "获取验证码", "get", "/captchaImage", {}, True, 200, "操作成功"]]
    # module, name, method, url, data,except_pt,except_code,except_result
    # 模块名称，用例名称，请求方式，链接，数据，成功断言，状态码断言，内容是否存在断言，非空断言不需要填写

    # 写入YAML文件
    with open('test_01.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, default_flow_style=True)

# write_yaml()

# def dict_read

def write_yaml1():
    # 要写入文件的数据
    data = [
        "test_01:",
        ["登录", "获取验证码", "get", "/captchaImage", {}, True, 200, '操作成功']
    ]
    # 写入YAML文件
    with open('test_01.yaml', 'w', encoding='utf-8') as file:
        file.writelines(data[0]+'\n')
    # 手动处理数据，以生成预期的 YAML 格式字符串
    yaml_str = ' - ['
    for item in data[1]:
        if isinstance(item, str):
            yaml_str += f'"{item}", '
        elif isinstance(item, bool):
            yaml_str += 'true, ' if item else 'false, '
        else:
            yaml_str += f'{item}, '
    yaml_str = yaml_str.rstrip(', ') + ']\n'
    # 写入文件
    with open('test_01.yaml', 'a', encoding='utf-8') as file:
        file.write(yaml_str)

write_yaml1()