#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import yaml
from flask import Blueprint, request, render_template
from flask import Flask,send_from_directory

simple = Blueprint('simple', __name__, template_folder='templates')


@simple.route('/submit', methods=['POST'])
def submit():
    # test_case = {
    #     'module_name': request.form['module_name'],
    #     'test_case_name': request.form['test_case_name'],
    #     'request_method': request.form['request_method'],
    #     'url': request.form['url'],
    #     'data': request.form['data'],
    #     'success_assertion': request.form['success_assertion'],
    #     'status_code_assertion': request.form['status_code_assertion'],
    #     'content_assertion': request.form['content_assertion'],
    #     'not_null_assertion': request.form['not_null_assertion']
    # }

    test_case = {request.form['module_name'],
         request.form['module_name'],request.form['test_case_name'],request.form['request_method'],request.form['url'],request.form['data'],request.form['success_assertion'],request.form['status_code_assertion'],request.form['content_assertion'],request.form['not_null_assertion']
    }

    with open('data_file/test_case1.yaml', 'a', encoding='utf-8') as file:
        yaml.dump([test_case], file, default_flow_style=False, allow_unicode=True)

    return 'Test case submitted successfully.'

@simple.route('/automation/interface')
def automation_interface():
    return render_template('test_case.html', content="接口管理页面内容")

# @simple.route('/test_case')
# def test_case():
#     return  render_template('index.html')

# @simple.route('/project_environment')
# def project_environment():
#     return render_template('project_environment.html')

@simple.route('/static_page')
def static_page():
    return send_from_directory('static', 'static_page.html')