#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import re
import time
import requests
from common.Send_Email import locathost_ip
from common.set_title import getrootdirectory
from common.yaml_util1 import load_ini

data_file_path = os.path.join(getrootdirectory(), 'config', 'setting.ini')
work_wechat = load_ini(data_file_path)["work_wechat"]
corpid = work_wechat['corpid']
corpsecret = work_wechat['corpsecret']
token_url = work_wechat['token_url']
program_url = work_wechat['program_url']
robot_url = work_wechat['robot_url']
state = work_wechat['state']
now_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())


def workwhat_access_token():
    params = {
        "corpid": corpid,
        "corpsecret": corpsecret
    }
    access_token = requests.get(token_url, params=params)
    # print(re.findall('access_token":"(.+?)"',access_token1)[0])
    return access_token.json()['access_token']


def send_workwhat(message):
    data = {
        "touser": "@all",
        "msgtype": "textcard",
        "agentid": 1000002,
        "textcard": {
            "title": "自动化监控报告",
            "description": "<div class=\"gray\">" + now_time + "</div> <div class=\"normal\">" + message + "</div><div class=\"highlight\">登录Jenkins查看报告详情</div>",
            "url": locathost_ip,
            "btntxt": "更多"
        },
        "safe": 0
    }
    new_url = program_url + '?access_token=' + workwhat_access_token()
    if state == 'True':
        send_program_message = requests.post(url=new_url, json=data)
        if send_program_message.status_code == 200:
            print("企业微信小程序消息推送成功！")


def send_workwhat_robot(message, result_type):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": "<font color=\"warning\">重庆农业产业数字化一张图监控</font>\n"
                       ">" + now_time + "\n"
                                        ">" + message + "\n"
                                                        ">[点击登录Jenkins查看报告详情](" + locathost_ip + ")\n"},
    }
    data1 = {
        "msgtype": "markdown",
        "markdown": {
            "content": "<font color=\"warning\">重庆农业产业数字化一张图监控</font>\n"
                       ">" + now_time + "\n"
                                        ">" + message + "\n"
                                                        ">[点击登录Jenkins查看报告详情](" + locathost_ip + ")\n"
                                                                                                 "<@ChenJiaWei><@Anna>"},
    }
    if state == 'True':
        if result_type == 0:
            send_robot_message = requests.post(robot_url, json=data)
            if send_robot_message.status_code == 200:
                print("群机器人消息发送成功！")
        elif result_type == 1:
            send_robot_message = requests.post(robot_url, json=data1)
            if send_robot_message.status_code == 200:
                print("群机器人消息发送成功！")
