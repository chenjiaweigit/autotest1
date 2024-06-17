#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import time

import allure
import pytest
from common.Log import log
from operation.keyword_request import keyword_request
from testcase.conftest import api_data
import json

class Test_login:

    @allure.epic("针对单个接口的测试")  # 标记功能分组 epic、feature、story包含关系的话是 从左到右，越来越小
    # @allure.feature("登录模块")   # 可根据个人需求增删，这几个标记用来给模块，用例等进行分组管理
    # @allure.story("用例--/用户登录/--预期成功")   # 被注释的为固定标题，可不修改
    # @allure.description("该用例是针对 监控{name}功能是否正常 场景的测试")  #用例描述
    @allure.severity(allure.severity_level.NORMAL)  # 用例优先级/严重等级
    @allure.issue("http://localhost:8080/job/pytest_demo1/", name="点击，跳转到对应BUG的链接地址")  # 问题链接
    @allure.testcase("http://localhost:8080/", name="点击，跳转到对应用例的链接地址")  # 用例链接  两个链接可根据情况自行添加
    @allure.title("{name}-预期成功")  # 用例标题
    @pytest.mark.parametrize("module,name,method,url,data,except_pt,except_code,except_result", api_data['test_01'])
    # @allure.step("测试登录成功")
    @pytest.mark.smoke   # smoke为标记用例可执行冒烟测试，可自定义名称
    @pytest.mark.run(order=1)  # 用例执行顺序，不添加就默认顺序执行
    def test_login(self, module, name, method, url, data, except_pt, except_code, except_result):
        allure.dynamic.feature("{}模块".format(module))
        allure.dynamic.story("用例--/{}/--预期成功".format(name))
        allure.dynamic.description("该用例是针对 监控\"{}\"功能是否正常 场景的测试".format(name))  # 用例描述
        # 用例步骤描述，暂时可不写
        with allure.step("步骤1 ==>> 登录用户：{}".format(data)):
            pass
        # step_1(data)
        log.info("*************** {}-开始执行用例 ***************".format(name))
        result = keyword_request(name=name, method=method, url=url, data=data)
        log.info("状态码 ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json()['code']))
        assert result.success == except_pt, log.info("成功断言失败：{}".format(result.error))
        assert result.response.status_code == except_code, log.info("状态码断言失败，except_code返回为：{}".format(except_code))
        assert result.response.json()['code'] == except_code
        log.info(f'{json.dumps(result.response.json(), sort_keys=True, indent=2)}')   #将返回以json格式输出
        log.info("except_result数据为：{}".format(except_result))
        assert str(except_result) in result.data, log.info("内容断言失败，接口返回为：{}".format(result.data))
        assert result.data != "", "数据返回为空"
        log.info("*************** {}-结束执行用例 ***************".format(name))