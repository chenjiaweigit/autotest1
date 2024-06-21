#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import yaml


def open_json():

    with open('static/data1.json','r',encoding = 'utf-8') as f:
        data = json.load(f)
    print(data)


def write_yaml():
    data1 = [{'id': 'c287d1a6-c7fc-49e2-a25c-1abb784f79c9',
              'caseNo': 'test001', 'templateName': '登录模块',
              'caseName': '登录测试', 'type': 'post',
              'address': '/login', 'params': '{username:admin;passdord:123456}',
              'success': 'Ture', 'status': '200', 'content': '测试',
              'notEmpty': '无1', 'LAY_NUM': 1, 'LAY_INDEX': 0},
             {'caseNo': 'test002', 'templateName': '注册模块',
              'caseName': '用户注册', 'type': 'post',
              'address': '/user/sign_in', 'params': '{username:user1;password:654321}',
              'success': 'Ture', 'status': '200', 'content': '注册成功',
              'notEmpty': '1', 'id': 'c066ae2a-d94a-4f77-9671-9f8d65040cc2',
              'LAY_NUM': 2, 'LAY_INDEX': 1}]
    # 要写入文件的数据
    # data = [
    #     ["test_01:",
    #     ["登录",
    #      "获取验证码",
    #      "get", "/captchaImage", {}, True, 200, "操作成功", "验证"]]
    # ]
    data = [['test001:', ['登录模块', '登录测试', 'post', '/login', {'username': 'admin', 'passdord': '123456'}, True, 200, '测试', '无1']], ['test002:', ['注册模块', '用户注册', 'post', '/user/sign_in', {'username': 'user1', 'password': '654321'}, 'Ture', '200', '注册成功', '1']]]
    # 定义一个标志变量
    is_first_write = True
    # 写入YAML文件
    for i in range(len(data)):
        mode = 'w' if is_first_write else 'a'
        with open('test_01.yaml', mode, encoding='utf-8') as file:
            file.writelines(data[i][0]+'\n')
        # 手动处理数据，以生成预期的 YAML 格式字符串
        yaml_str = ' - ['
        for item in data[i][1]:
            if isinstance(item, str):
                yaml_str += f'"{item}", '
            elif isinstance(item, bool):
                yaml_str += 'True, ' if item else 'False, '
            else:
                yaml_str += f'{item}, '
        yaml_str = yaml_str.rstrip(', ') + ']\n'
        # 写入文件
        with open('test_01.yaml', 'a', encoding='utf-8') as file:
            file.write(yaml_str)
        # 只在第一次写入时使用覆盖写入模式
        is_first_write = False

# write_yaml()

data1 = [{'id': 'c287d1a6-c7fc-49e2-a25c-1abb784f79c9', 'caseNo': 'test001',
          'templateName': '登录模块', 'caseName': '登录测试', 'type': 'post',
          'address': '/login', 'params': '{username:admin;passdord:123456}',
          'success': '200', 'status': '200', 'content': '测试',
          'notEmpty': '无1', 'LAY_NUM': 1, 'LAY_INDEX': 0},
         {'caseNo': 'test002', 'templateName': '注册模块', 'caseName': '用户注册',
          'type': 'post', 'address': '/user/sign_in',
          'params': '{username:user1;password:654321}', 'success': '200',
          'status': '200', 'content': '注册成功', 'notEmpty': '1',
          'id': 'c066ae2a-d94a-4f77-9671-9f8d65040cc2', 'LAY_NUM': 2, 'LAY_INDEX': 1},
         {'caseNo': 'test_003', 'templateName': '首页', 'caseName': '输入框查询',
          'type': 'get', 'address': '/getata/test', 'params': '{username:user2;password:654321}', 'success':
              'True', 'status': '200', 'content': '查询成功', 'notEmpty': '123456',
          'id': '0fbb6f0b-2efb-499e-93d8-1e89a2406549', 'LAY_NUM': 3, 'LAY_INDEX': 2}]



def parse_params(param_str):
    # Remove the curly braces
    param_str = param_str.strip('{}')
    # Split the string by semicolon
    param_pairs = param_str.split(';')
    # Split each pair by colon and convert to dictionary
    params = {}
    for pair in param_pairs:
        key, value = pair.split(':')
        params[key.strip()] = value.strip()
    return params

def transform_data(data1):
    data = []
    for item in data1:
        transformed_item = [
            f"{item['caseNo']}:",
            [
                item['templateName'],
                item['caseName'],
                item['type'],
                item['address'],
                parse_params(item['params']),  # Convert params to a dictionary
                item['success'],
                item['status'],
                item['content'],
                item['notEmpty']
            ]
        ]
        data.append(transformed_item)
    return data

data = transform_data(data1)
# print(data)
# print("="*25,"开始运行pytest测试框架","="*25)

numbers = "200"
b = ['200','400','500']
a = [True if '200' in b else 300]
# print([True if '200' in b else 300][0])
def te1():
    try:
        a = 2
        print(a)
    except Exception as e:
        return 1
    except ValueError as ve:
        return 2
    else:
        print(1111)


def generate_test_script(test_cases):
    script_content = """#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import allure
import pytest

from common.Log import log
from operation.keyword_request import keyword_request
from testcase.conftest import api_data


@allure.severity(allure.severity_level.NORMAL)
@allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")
@allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
@allure.title("{name}-预期成功")
@pytest.mark.smoke1
@pytest.mark.run(order=4)
@pytest.mark.parametrize("module,name,method,url,data,except_pt,except_code,except_result", api_data['test_04'])
def test_1(module, name, method, url, data, except_pt, except_code, except_result):
    allure.dynamic.feature("{}模块".format(module))
    allure.dynamic.story("用例--/{}/--预期成功".format(name))
    allure.dynamic.description("该用例是针对 监控{name}功能是否正常 场景的测试")

    log.info("*************** {}-开始执行用例 ***************".format(name))
    result = keyword_request(name=name, method=method, url=url, data=data)
    log.info("状态码 ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get('data',{}).get('code')))
    assert result.success == except_pt, log.info("断言失败：{}".format(result.error))
    assert result.response.status_code == except_code, log.info("断言失败，except_code返回为：{}".format(except_code))
    # log.info(f'{json.dumps(result.response.json(), sort_keys=True, indent=2)}')
    log.info("except_result数据为：{}".format(except_result))
    assert str(except_result) in result.data, log.info("断言失败：{}".format(except_result))
    assert result.data != "", log.info("断言失败：data数据返回为空>>{}".format(result.data))
    result.data1 = eval(result.data)
    assert result.data1["data"]["mean"] != "",log.info("断言失败：mean数据返回为空>>{}".format(result.data))
    log.info("*************** {}-结束执行用例 ***************".format(name))
"""
    print(script_content)


import time,os
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


log_file_path = r'D:\python_project\Flask代码\untitled1\autotest1\log\20240618.log'

def read_log():
    print(f"日志文件路径：{log_file_path}")
    with open(log_file_path, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                print(f"读取到日志：{line.strip()}")
                # socketio.emit('log', {'message': line.strip()})
            else:
                time.sleep(0.1)
            f.seek(0, 2)  # 将文件指针移动到文件末尾

# directory = 'log'  # 替换为你的目录路径

