# -*- coding:utf-8 -*-
# @datetime:2019/4/17 20:49
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:conf_url.py
from common.read_config import ReadConfig


class ConfUrl:
    """通过switch开关及test和online文件的配置来确定url"""
    def __init__(self):
        self.config = ReadConfig('switch_url', 'on')

    def get_url(self):
        return self.config.get_contents('api', 'url')


if __name__ == '__main__':
    conf_url = ConfUrl()
    print(conf_url.get_url())


