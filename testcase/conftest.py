#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
import pytest
from common.Log import log
from common.Send_Email import Send_email
from common.WorkWeChat import send_workwhat, send_workwhat_robot
from common.serverchanConf import sendServerChan
from common.yaml_util1 import clear_yaml, read_yamlcase
import time

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(BASE_PATH, "data_file", yaml_file_name)
        yaml_data = read_yamlcase(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


api_data = get_data("test_case.yaml")


@pytest.fixture(scope="session", autouse=True)
def execute_database_sql():
    log.info("~~~~~~~~~~在所有请求之前执行一次~~~~~~~~~~~")
    clear_yaml('/extract_token.yaml')
    yield
    log.info("~~~~~~~~~~在所有请求之后执行一次~~~~~~~~~~~")


@pytest.fixture(scope="function")
# 获取用例函数名称
def testcase_data(request):
    testcase_name = request.function.__name__
    return api_data.get(testcase_name)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # 收集测试结果
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    deselected = len(terminalreporter.stats.get('deselected', []))
    rerun = len(terminalreporter.stats.get('rerun', []))
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    email_list = {'用例总数': total, '通过': passed, '失败': failed, '错误': error, '跳过': skipped, '省略': deselected,
                  '重试':rerun,'总运行时间': duration}
    Send_email(result=email_list).mail()
    sum_list = ("用例总数: {}\n "
                "通过： {}\n "
                "失败： {}\n "
                "错误： {}\n "
                "跳过： {}\n "
                "省略： {}\n "
                "重试： {}\n "
                "总运行时间： {:.3f}s".format(total, passed, failed, error, skipped, deselected, rerun, duration))
    # send_workwhat(sum_list)
    if failed == 0:
        send_workwhat_robot(sum_list, 0)
    elif failed > 0:
        send_workwhat_robot(sum_list, 1)


    if failed > 0:
        sendServerChan(sum_list)

    print("===============pytest_terminal_summary===================")
    # print(terminalreporter.stats)
    print("用例总数:", terminalreporter._numcollected)
    print('通过:', len(terminalreporter.stats.get('passed', [])))
    print('失败:', len(terminalreporter.stats.get('failed', [])))
    print('错误:', len(terminalreporter.stats.get('error', [])))
    print('跳过:', len(terminalreporter.stats.get('skipped', [])))
    print('省略:', len(terminalreporter.stats.get('deselected', [])))
    print('重试:', len(terminalreporter.stats.get('rerun', [])))
    # terminalreporter._sessionstarttime 会话开始时间
    # duration = time.time() - terminalreporter._sessionstarttime
    print('总运行时间:', duration, 'seconds')
    print('开始时间', round(terminalreporter._sessionstarttime))
    print('现在时间', round(time.time()))
    print(round(time.time() - terminalreporter._sessionstarttime))
