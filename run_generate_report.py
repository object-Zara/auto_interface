# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:17
# @author:1111
# @email:123@sina.com
# @File:run_generate_report.py
import unittest
import datetime
import os
from BeautifulReport import BeautifulReport
from common import get_path


class GenerateReport:
    """完成测试用例执行并生成测试报告"""
    @staticmethod
    def generate_report():
        suite = unittest.TestSuite()

        case_path = get_path.GetPath().get_testcases_path()
        discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py")

        suite.addTest(discover)

        runner = BeautifulReport(suite)
        filename = datetime.datetime.now().strftime('%Y-%m-%d')+'-测试报告'
        log_path = os.path.join(os.getcwd(), 'test_result', 'html_report')
        runner.report(description='Http请求的测试报告', filename=filename, log_path=log_path)


if __name__ == '__main__':
    GenerateReport().generate_report()

