# -*- coding: utf8 -*-

import os
from common.set_title import getrootdirectory
from common.yaml_util1 import load_ini
from operation.all_requests import new_requests

data_file_path = os.path.join(getrootdirectory(),'config','setting.ini')
server_message = load_ini(data_file_path)["server_conf"]


def sendServerChan(msg):
        """
        server酱微信通知
        : _key 需要去server酱进行申请，https://sct.ftqq.com/
        :param str: 通知内容 content
        :return:
        """
        sendServerChanUrls = server_message["push_server_path"].strip()
        if (
            server_message["is_server_chan"] == 'True'
            and server_message["secret"].strip() != ""
        ):
            secret = server_message["secret"].strip()
            sendServerChanUrls += f'{secret}.send'
            params = {"title": "自动化测试结果", "desp": msg}
            sendServerChanRsp = new_requests.get(url=sendServerChanUrls, data=params)

            try:
                if sendServerChanRsp.json()['code'] == 0:
                    pushid = sendServerChanRsp.json()['data']['pushid']
                    readkey = sendServerChanRsp.json()['data']['readkey']
                    url = f'{sendServerChanUrls}push'
                    params = f'id={pushid}&readkey={readkey}'
                    new_requests.get(url=url,data=params)
                    print(u"已下发 Server酱 微信通知, 请查收")
                    # log.info(f'{json.dumps(push_start.json(), sort_keys=True, indent=2)}')
                    return True
                else:
                    print(sendServerChanRsp)
                    return False
            except Exception as e:
                print(u"Server酱 配置有误 {} 或已达到今日发送次数上限.....".format(e))
