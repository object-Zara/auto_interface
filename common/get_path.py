# -*- coding:utf-8 -*-
# @datetime:2019/4/1 22:51
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:get_path.py

from configparser import ConfigParser


class GetPath:
    def __init__(self):
        self.cf = ConfigParser()
        self.cf.read(r'E:\PycharmProjects\A_auto_test_interface\conf\path_conf.cfg', encoding='utf-8')

    def get_logging_path(self):
        return self.cf['path']['logging_path']

    def get_email_info_path(self):
        return self.cf['path']['email_info_path']

    def get_test_case_path(self):
        return self.cf['path']['test_case_path']

    def get_report_path(self):
        return self.cf['path']['report_path']

    def get_email_report_path(self):
        return self.cf['path']['email_report_path']


if __name__ == '__main__':
    get_path = GetPath().get_email_info_path()
    print(get_path)



