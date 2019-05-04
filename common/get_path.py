# -*- coding:utf-8 -*-
# @datetime:2019/4/1 22:51
# @author:123
# @email:1111@sina.com
# @File:get_path.py
import os


class GetPath:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def get_conf_logging_path(self):
        return os.path.join(self.base_dir, 'conf', 'logging_config.cfg')

    def get_logging_path(self):
        return os.path.join(self.base_dir, 'test_result', 'log')

    def get_email_info_path(self):
        return os.path.join(self.base_dir, 'test_data', 'email_info.xlsx')

    def get_testcases_path(self):
        return os.path.join(self.base_dir, 'test_case')

    def get_test_case_data_path(self):
        return os.path.join(self.base_dir, 'test_data', 'future_interface.xlsx')

    def get_report_path(self):
        return os.path.join(self.base_dir, 'test_result', 'html_report')

    def get_conf_url(self):
        return os.path.join(self.base_dir, 'conf', 'switch_on.cfg')

    def get_online_url(self):
        return os.path.join(self.base_dir, 'conf', 'online_config.cfg')

    def get_test_url(self):
        return os.path.join(self.base_dir, 'conf', 'test_conf.cfg')


if __name__ == '__main__':
    get_path = GetPath()
    print(get_path.get_online_url())
    print(get_path.get_test_case_data_path())
    # res = get_path.get_logging_path()
    # res2 = get_path.get_email_info_path()
    # res3 = get_path.get_test_case_path()
    # res4 = get_path.get_report_path()
    # print(res, res2, res3, res4)



