# -*- coding:utf-8 -*-
""" 
@datetime:2019/4/21 18:55
@author:123
@email:1111@sina.com
@File:read_config.py 
@function： 读取配置文件
"""
from configparser import ConfigParser
from common.get_path import GetPath


class ReadConfig:
    def __init__(self, switch, on):
        self.config = ConfigParser()
        path_switch = GetPath().get_conf_url()
        self.config.read(path_switch)  # 先加载global
        self.switch = self.config.getboolean(switch, on)

    def get_contents(self, section, option):
        path_test = GetPath().get_test_url()
        path_online = GetPath().get_online_url()
        if self.switch:  # 开关打开的时候，使用online的配置
            self.config.read(path_online, encoding='utf-8')
        else:  # 开关关闭的时候，使用test的配置
            self.config.read(path_test, encoding='utf-8')
        return self.config.get(section, option)


if __name__ == '__main__':
    res = ReadConfig('switch_data', 'on').get_contents('user_data', 'normal_user')
    print(res)
