#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json as complexjson
import requests
from common.Log import log

class AllRequests():

    def get(self, url, **kwargs):
        return self.all_send_requests(url, "GET", **kwargs)

    def post(self, url, data=None, json=None,headers=None, **kwargs):
        return self.all_send_requests(url, "POST", data, json, headers,**kwargs)

    def put(self, url, data=None, **kwargs):
        return self.all_send_requests(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.all_send_requests(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.all_send_requests(url, "PATCH", data, **kwargs)
    def all_send_requests(self,url,method,data=None,json=None,**kwargs):
        # headers = dict(**kwargs).get("headers")
        url =url
        params = dict(**kwargs).get("params")
        files = dict(**kwargs).get("params")
        cookies = dict(**kwargs).get("params")
        method = str(method).lower()
        # re = None
        self.request_log(url, method, data, json, params, files, cookies)
        if method == 'get':
            return requests.request(method=method,url=url,params=data,**kwargs)
        elif method == 'post':
            # strdata = json.dumps(data)
            return requests.request(method=method, url=url, json=data,**kwargs)
        elif method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            return self.put(url, data, **kwargs)
        elif method == "DELETE":
            return self.delete(url, **kwargs)
        elif method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            return self.session.patch(url, data, **kwargs)
        else:
            print("不支持的请求方式....")

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None, **kwargs):
        log.info("接口请求地址 ==>> {}".format(url))
        log.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        log.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        log.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        log.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        log.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        log.info("接口上传附件 files 参数 ==>> {}".format(files))
        log.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))

new_requests = AllRequests()
