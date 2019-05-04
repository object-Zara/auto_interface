# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:25
# @author:123
# @email:1111@sina.com
# @File:http_request.py
from requests import sessions
from common.conf_url import ConfUrl
from common.my_logging import Mylogging


class MyRequest:
    def __init__(self):
        self.session = sessions.Session()
        conf_url = ConfUrl()
        self.url = conf_url.get_url()
        self.loger = Mylogging()

    def request(self, method, url, data=None, json=None):
        url = self.url + url
        if type(data) == str:
            data = eval(data)  # str转成字典

        self.loger.get_log('info', '请求的参数为{},“{}”'.format(url, data))

        if method.upper() == "GET":
            try:
                return self.session.request(method, url, params=data)
            except Exception as e:
                print('get请求出错：{}'.format(e))
                return e
        elif method.upper() == "POST":
            try:
                if json:
                    return self.session.request(method, url, data=json)
                else:
                    return self.session.request(method, url, data=data)
            except Exception as e:
                print('post请求出错：{}'.format(e))
                return e
        else:
            print('既不是get也不是post请求')
            return '既不是get也不是post请求'

    def session_close(self):
        self.session.close()


if __name__ == '__main__':
    myrequest = MyRequest()

    # 注册接口
    url_register = '/member/register'
    param = {"mobilephone": "15019215377", "pwd": "123456"}
    res = myrequest.request('post', url=url_register, data=param)
    print(res.text)

    # 登录接口
    # url_login = '/member/login'
    # param = {"mobilephone": "15019215377", "pwd": "123456"}
    # myrequest.request('post', url=url_login, data=param)
    # # 充值接口
    # url_recharge = '/member/recharg'
    # param = {"mobilephone": "15019215377", "amount": "100"}
    # resp_recharge = myrequest.request('post', url=url_recharge, data=param)
    # # print(json.loads(resp_recharge.text)["msg"])
    # print(resp_recharge.text)
    # print(type(resp_recharge.text))

    # 增加项目接口
    # url_add = '/loan/add'
    # # param = {"memberId": "878","title": "买车","amount": 20000,"loanRate": "12.0",
    # #          "loanTerm": 3,"loanDateType": 0,"repaymemtWay": 11,"biddingDays": 5}
    # param ={"memberId": "FFFF","title": "买车","amount": 20000,"loanRate": "12.0","loanTerm": 3,
    #         "loanDateType": 0, "repaymemtWay": 11,"biddingDays": 6}
    # res = myrequest.request('post',url=url_add,data=param)

    # 投资接口
    # url_invest = '/member/bidLoan'
    # param = {'memberId': 2714, 'password': '123456', 'loanId': 32, 'amount': 200}
    # res = myrequest.request('post', url=url_invest, data=param)
    # print(res.text)

    myrequest.session_close()
