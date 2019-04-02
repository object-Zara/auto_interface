# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:25
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:http_request.py


import requests


class HttpRequest:
    @staticmethod
    def http_request(method, url, param, cookie=None):
        if method.upper() == "GET":
            try:
                return requests.get(url, params=param)
            except Exception as e:
                print('get请求出错：{}'.format(e))
                return e
        elif method.upper() == "POST":
            try:
                return requests.post(url, param)
            except Exception as e:
                print('get请求出错：{}'.format(e))
                return e
        else:
            print('既不是get也不是post请求')
            return '既不是get也不是post请求'


if __name__ == '__main__':
    url_request = 'http://47.107.168.87:8080/futureloan/mvc/api/member/register'
    param_request = {"mobilephone": "15019215373", "pwd": "123457"}
    request_1 = HttpRequest()
    resp = request_1.http_request('get', url_request, param_request)
    print(resp.text)
    print(type(resp.text))
    print(resp.json())
    print(type(resp.json()))


