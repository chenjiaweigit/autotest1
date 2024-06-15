#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import re,json

from common.Log import log
from common.set_title import getrootdirectory
from common.yaml_util1 import read_yaml_token, write_yaml, load_ini
from operation.ResultBase import ResultBase
from operation.all_requests import new_requests

data_file_path = os.path.join(getrootdirectory(), "config", "setting.ini")
api_root_url = load_ini(data_file_path)["host"]["api_root_url"]
lerc_token = load_ini(data_file_path)["host"]["lerc_token"]
lerc_url = load_ini(data_file_path)["host"]["lerc_url"]

def keyword_request(name,method,url,data):
    """
    获取所有结果
    :return: 自定义的关键字返回结果 result
    """
    result = ResultBase()
    method = method
    # url = api_root_url + url
    data = data
    name = name
    if read_yaml_token() == None and "lerc" not in url:
        header = None
        url = api_root_url + url
    elif "lerc" in url:
        url = lerc_url + url
        header = {"token": lerc_token}
    else:
        url = api_root_url + url
        header = read_yaml_token()
    res = new_requests.all_send_requests(method=method,url=url,data=data,headers=header)
    result.success = False


    if res.status_code == 200:
        result.success = True
    else:
        result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.status_code, res.json())
    try:
        if 'token' in res.text:
            '''
            不同的项目研发代码编写格式不同，所以token无法统一获取，需根据实际情况进行提取，
            目前有返回json字典提取和正则提取，自行选择一种进行操作，不需要可忽略...
            '''
            token_values = {'token': res.json()['data']['token']}
            # token_values = {'token': re.findall(f'"token":"(.+?)","i',res.text)[0]}
            write_yaml(token_values, yaml_file='/extract_token.yaml')
    except Exception as e:
        log.info("token获取失败失败{}".format(e))
    result.data = res.text
    if "lerc" not in url:
        log.info("请求返回信息 >>> {}".format(res.text))
    else:
        log.info("lerc数据请求返回过大暂不返回！！！")
    # result.json = re.text
    log.info("resulr.data数据为:{}".format(result.success))
    result.response = res
    log.info("{} ==>> 返回状态码为 >> {}".format(name,result.response.status_code))
    # log.info("json.get方法获取状态码{}".format(result.response.json().get('data',{}).get('code')))
    return result


