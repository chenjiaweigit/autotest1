#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os

from flask import Blueprint, request, render_template, jsonify
from flask import Flask,send_from_directory
from common.Log import log
import subprocess
from common.yaml_util1 import modify_ini_and_write

simple = Blueprint('simple', __name__, template_folder='templates')

def parse_params(param_str):
    """
    # Remove the curly braces
    param_str = param_str.strip('{}')
    # Split the string by semicolon
    param_pairs = param_str.split(';')
    # Split each pair by colon and convert to dictionary
    params = {}
    for pair in param_pairs:
        key, value = pair.split(':', 1)
        params[key.strip()] = value.strip()
    return params"""
    param_str = param_str.replace('\'', '"')  # Replace single quotes with double quotes if necessary
    params_list = json.loads(f'[{param_str}]')  # Wrap the string in square brackets to create a list
    params = {}
    for param in params_list:
        params.update(param)
    return params


def transform_data(getdata):
    data = []
    for item in getdata:
        if item['params'] == "" or item['params'] == "{}"\
                and item['notEmpty'].lower() == "none":
            transformed_item = [
                f"{item['caseNo']}:",
                [
                    item['templateName'],
                    item['caseName'],
                    item['type'],
                    item['address'],
                    {},  # Convert params to a dictionary
                    [True if str(item['success']).lower() == 'true' else False][0],
                    int(item['status']),
                    item['content'],
                ]
            ]
        elif item['params'] == "" or item['params'] == "{}" \
                and item['notEmpty'].lower() != "none":
            transformed_item = [
                f"{item['caseNo']}:",
                [
                    item['templateName'],
                    item['caseName'],
                    item['type'],
                    item['address'],
                    {},  # Convert params to a dictionary
                    [True if str(item['success']).lower() == 'true' else False][0],
                    int(item['status']),
                    item['content'],
                    item['notEmpty']
                ]
            ]
        elif item['notEmpty'].lower() == "none":
            transformed_item = [
                f"{item['caseNo']}:",
                [
                    item['templateName'],
                    item['caseName'],
                    item['type'],
                    item['address'],
                    parse_params(item['params']),
                    [True if str(item['success']).lower() == 'true' else False][0],
                    int(item['status']),
                    item['content'],
                ]
            ]
        else:
            transformed_item = [
                f"{item['caseNo']}:",
                [
                    item['templateName'],
                    item['caseName'],
                    item['type'],
                    item['address'],
                    parse_params(item['params']),  # Convert params to a dictionary
                    [True if str(item['success']).lower() == 'true' else False][0],
                    int(item['status']),
                    item['content'],
                    item['notEmpty']
                ]
            ]
        data.append(transformed_item)
    return data


@simple.route('/submit', methods=['POST'])
def submit():
    """
    解析json数据，写入测试用例
    :return:
    """
    objects = request.get_json(force=True)
    log.info("{}".format(objects))
    try:
        data = transform_data(objects)
    except Exception as e:
        log.error(e)
    else:
        for filename in os.listdir('testcase'):
            if filename.startswith('test') and filename.endswith('.py'):
                filepath = os.path.join('testcase', filename)
                os.remove(filepath)
                print(f"Deleted: {filepath}")
        log.info(f'解析后的数据==>> {data}')
    # print(data[1]['caseNo'])
    # 定义一个标志变量
    is_first_write = True
    # 写入YAML文件
    try :
        for case_list in range(len(data)):
            mode = 'w' if is_first_write else 'a'
            with open('data_file/test_case.yaml', mode, encoding='utf-8') as file:
                file.writelines(data[case_list][0] + '\n')
            # 手动处理数据，以生成预期的 YAML 格式字符串
            
            yaml_str = ' - ['
            for item in data[case_list][1]:
                if isinstance(item, str):
                    yaml_str += f'"{item}", '
                elif isinstance(item, bool):
                    yaml_str += 'True, ' if item else 'False, '
                else:
                    yaml_str += f'{item}, '
            yaml_str = yaml_str.rstrip(', ') + ']\n'
            # 写入文件
            with open('data_file/test_case.yaml', 'a', encoding='utf-8') as file:
                file.write(yaml_str)
            # 只在第一次写入时使用覆盖写入模式
            is_first_write = False
            generate_test_script(data[case_list][0], case_list)
    except Exception as e:
        log.error("{}".format(e))
    else:
        log.info("用例写入yaml文件完成！")
    # case_status = {'data_num':len(data),'status':'Test case submitted successfully.'}
    # return case_status
    return 'Test case submitted successfully.'


def generate_test_script(test_cases, casefile_list):
    # casefile_list_New
    script_content1 = '''#!/usr/bin/env python
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
@pytest.mark.run(order=4)'''
    script_content2 = f'''
@pytest.mark.parametrize("module,name,method,url,data,except_pt,except_code,except_result", api_data['{test_cases.split(':')[0]}'])
def {test_cases.split(':')[0]}(module, name, method, url, data, except_pt, except_code, except_result):'''
    script_content3 = '''
    allure.dynamic.feature("{}模块".format(module))
    allure.dynamic.story("用例--/{}/--预期成功".format(name))
    allure.dynamic.description("该用例是针对 监控{name}功能是否正常 场景的测试")
    
    log.info("*************** {}-开始执行用例 ***************".format(name))
    result = keyword_request(name=name, method=method, url=url, data=data)
    log.info("状态码 ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get('data',{}).get('code')))
    assert result.success == except_pt, log.info("成功断言失败：{}".format(result.error))
    assert result.response.status_code == except_code, \
        log.info("状态码断言失败，期望值：{}，接口返回为：{}".format(except_code, result.response.status_code))
    log.info("except_result数据为：{}".format(except_result))
    assert str(except_result) in result.data, \
        log.info("内容断言失败，期望值：{}，接口返回为：{}".format(str(except_result), result.data))
    assert result.data != "", log.info("断言失败：data数据返回为空>>{}".format(result.data))
    # result.data1 = eval(result.data)
    # assert result.data1 != "",log.info("断言失败：mean数据返回为空>>{}".format(result.data))
    log.info("*************** {}-结束执行用例 ***************".format(name))
'''
    casefile_Name = f'testcase/test_api{casefile_list}.py'
    with open(casefile_Name, 'w', encoding='utf-8') as file:
        file.write(script_content1 + script_content2 + script_content3)
        log.info(f"Test script generated successfully==>{casefile_Name}")


@simple.route('/automation/interface')
def automation_interface():
    return render_template('test_case.html', content="接口管理页面内容")


@simple.route('/static_page')
def static_page():
    return send_from_directory('static', 'static_page.html')


@simple.route('/run_pytest', methods=['POST'])
def run_tests():

    """
    # 打印请求头
    print("Headers: ", request.headers)
    # 打印请求数据
    print("Data: ", request.data)
    # 打印 JSON 数据
    print("JSON: ", request.get_json())
    """
    try:
        # 获取原始字符串数据
        temp_domains = request.data.decode('utf-8')
        if not temp_domains:
            raise ValueError("Empty data received")
        # 处理 temp_domains 写入setting.ini配置文件
        if modify_ini_and_write('host', 'api_root_url', temp_domains):
            # 运行pytest框架
            log.info("="*25 + "开始运行Pytest测试框架" + "="*25)
            subprocess.run(['python', 'run.py'])
        result = {"status": "success", "message": "Test started"}
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # 捕获所有其他异常
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

