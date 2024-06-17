#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json

from flask import Blueprint, request, render_template, jsonify
from flask import Flask,send_from_directory
from common.Log import log
import subprocess
from common.yaml_util1 import modify_ini_and_write

simple = Blueprint('simple', __name__, template_folder='templates')

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
                    [True if item['success'].lower() == 'true' else True][0],
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
                    [True if item['success'].lower() == 'true' else True][0],
                    int(item['status']),
                    item['content'],
                    item['notEmpty']
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
                    [True if item['success'].lower() == 'true' else True][0],
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
    data = transform_data(objects)
    print(data)

    # 定义一个标志变量
    is_first_write = True
    # 写入YAML文件
    try :
        for i in range(len(data)):
            mode = 'w' if is_first_write else 'a'
            with open('data_file/test_case.yaml', mode, encoding='utf-8') as file:
                file.writelines(data[i][0] + '\n')
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
            with open('data_file/test_case.yaml', 'a', encoding='utf-8') as file:
                file.write(yaml_str)
            # 只在第一次写入时使用覆盖写入模式
            is_first_write = False
    except Exception as e:
        log.error("{}".format(e))
    else:
        log.info("用例写入yaml文件完成！")

    return 'Test case submitted successfully.'


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
            log.info("="*25 + "开始运行pytest测试框架" + "="*25)
            subprocess.run(['python', 'run.py'])
        result = {"status": "success", "message": "Test started"}
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # 捕获所有其他异常
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

