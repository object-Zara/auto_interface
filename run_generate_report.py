# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:17
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:run_generate_report.py
import unittest
import datetime
from BeautifulReport import BeautifulReport
from test_case import test_httprequest
from common import get_path


class GenerateReport:
    @staticmethod
    def generate_report():
        suite = unittest.TestSuite()
        loder = unittest.TestLoader()

        suite.addTest(loder.loadTestsFromModule(test_httprequest))

        runner = BeautifulReport(suite)
        filename = datetime.datetime.now().strftime('%Y-%m-%d')+'-测试报告'
        runner.report(description='Http请求的测试报告', filename=filename, log_path=get_path.GetPath().get_report_path())


if __name__ == '__main__':
    GenerateReport().generate_report()

