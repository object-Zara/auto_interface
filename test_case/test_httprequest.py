# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:59
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:test_httprequest.py

import unittest
import json
from ddt import ddt, unpack, data
from common import http_request
from common import do_excel
from common import my_logging
from common import get_path

"""从excel读取数据"""
data_doexcel = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_path()).read_data('httprequest')
loger = my_logging.Mylogging()


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        self.t = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_path())

    @data(*data_doexcel)
    @unpack
    def test_httprequest(self, case_id, name, method, url, param, expect):
        """对login接口请求的测试"""
        loger.get_log('info', '************************************')
        loger.get_log('info', '正在执行第{}条用例“{}”'.format(case_id, name))
        loger.get_log('info', '请求的数据是：{}'.format(data_doexcel[int(case_id)-1]))
        request_result = http_request.HttpRequest().http_request(method, url, param)
        try:
            self.assertEqual(expect, request_result.json())
            testresult = 'pass'
        except AssertionError as e:
            testresult = 'failed'
            loger.get_log('error', '第{}条用例“{}”出错{}'.format(case_id, name, e))
            # loger.get_log('error', '出错{}'.format(testresult))
            raise e
        finally:
            loger.get_log('info', '********开始将结果写回excel数据********')
            self.t.write_data('httprequest', int(case_id) + 1, 7, json.dumps(request_result.json()))
            self.t.write_data('httprequest', int(case_id)+1, 8, testresult)
            loger.get_log('info', '********结束将结果写回excel数据********')


if __name__ == '__main__':
    unittest.main(verbosity=2)

