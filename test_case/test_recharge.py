# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:59
# @author:123
# @email:1111@sina.com
# @File:test_httprequest.py
import json
import unittest
from ddt import ddt, data
from common import http_request
from common import do_excel
from common import my_logging
from common import get_path
from common import do_sql

"""从excel读取数据"""
sheet_name = 'recharge'
data_doexcel = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path()).read_data(sheet_name)
loger = my_logging.Mylogging()


@ddt
class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.MyRequest()
        cls.t = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path())
        cls.sql = do_sql.DoSql()

    @data(*data_doexcel)
    def test_recharge(self, case):
        """对recharge接口请求的测试"""
        global testresult
        if case.case_excute.upper() == "NO":
            self.skipTest('该条用例不执行')
        loger.get_log('info', '************************************')
        loger.get_log('info', '正在执行第{}条用例“{}”'.format(case.case_id, case.title))
        if case.data.find('#mobilephone#') != -1:  # 判断参数化的标识
            sql = 'select max(mobilephone) from future.member'
            mobilephone = self.sql.do_sql(sql, 'one')['max(mobilephone)']
            if case.title == '正常注册' or case.title == '手机号未注册':
                # 最大手机号码+1
                mobilephone = int(mobilephone) + 1
            case.data = case.data.replace('#mobilephone#', str(mobilephone))  # 替换参数值
            if case.title == '正常充值':
                sql = 'select * from future.member where mobilephone =(SELECT mobilephone from future.member ORDER BY ID LIMIT 1)'
                member = self.sql.do_sql(sql, 'one')
                before = member['LeaveAmount']
        request_result = self.http_request.request(case.method, case.url, data=case.data).text
        try:
            if case.title == '正常充值':
                sql = 'select * from future.member where mobilephone =(SELECT mobilephone from future.member ORDER BY ID LIMIT 1)'
                member = self.sql.do_sql(sql, 'one')
                after = member['LeaveAmount']
                recharge_amount = int(eval(case.data)['amount'])  # 充值金额
                if self.assertEqual(before + recharge_amount, after):
                    testresult = 'pass'
                else:
                    testresult = 'fail'
            else:
                self.assertEqual(case.expect, json.loads(request_result)["msg"])
                testresult = 'pass'
        except AssertionError as e:
            testresult = 'failed'
            loger.get_log('error', '第{}条用例“{}”出错{}'.format(case.case_id, case.title, e))
            raise e
        finally:
            loger.get_log('info', '********开始将结果写回excel数据********')
            self.t.write_data(sheet_name, int(case.case_id) + 1, 8, request_result)
            self.t.write_data(sheet_name, int(case.case_id)+1, 9, testresult)
            loger.get_log('info', '********结束将结果写回excel数据********')

    @classmethod
    def tearDownClass(cls):
        cls.sql.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)

