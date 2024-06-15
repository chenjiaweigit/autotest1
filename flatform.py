#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from flask import Blueprint, request, render_template
from flask import Flask,send_from_directory

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


@simple.route('/submit', methods=['POST'])
def submit():
    """
    解析json数据，写入测试用例
    :return:
    """
    objects = request.get_json(force=True)
    print(objects)
    data = transform_data(objects)

    # 定义一个标志变量
    is_first_write = True
    # 写入YAML文件
    for i in range(len(data)):
        mode = 'w' if is_first_write else 'a'
        with open('date_file/test_case1.yaml', mode, encoding='utf-8') as file:
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
        with open('date_file/test_case1.yaml', 'a', encoding='utf-8') as file:
            file.write(yaml_str)
        # 只在第一次写入时使用覆盖写入模式
        is_first_write = False

    return 'Test case submitted successfully.'


@simple.route('/automation/interface')
def automation_interface():
    return render_template('test_case.html', content="接口管理页面内容")


@simple.route('/static_page')
def static_page():
    return send_from_directory('static', 'static_page.html')
