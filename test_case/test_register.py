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
sheet_name = 'register'
data_doexcel = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path()).read_data(sheet_name)
loger = my_logging.Mylogging()


@ddt
class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.MyRequest()
        cls.t = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path())
        cls.sql = do_sql.DoSql()

    @data(*data_doexcel)
    def test_register(self, case):
        """对register接口请求的测试"""
        global result
        if case.case_excute.upper() == "NO":
            self.skipTest('该条用例不执行')
        loger.get_log('info', '************************************')
        loger.get_log('info', '正在执行第{}条用例“{}”'.format(case.case_id, case.title))
        if case.data.find('#mobilephone#') != -1:  # 判断参数化的标识
            sql = 'select max(mobilephone) as MaxMobilePhone from future.member'
            mobilephone = self.sql.do_sql(sql, 'one')['MaxMobilePhone']
            if case.title == '重复注册':
                case.data = case.data.replace('#mobilephone#', mobilephone)
            else:
                # 最大手机号码+1
                max_phone = int(mobilephone) + 1
                # replace方法是替换之后重新返回一个新的字符串，所以需要使用case.data重新接收
                case.data = case.data.replace('#mobilephone#', str(max_phone))  # 替换参数值
        request_result = self.http_request.request(case.method, case.url, data=case.data).text
        try:
            self.assertEqual(case.expect, request_result)
            if json.loads(request_result)['msg'] == '注册成功':
                sql = 'select Mobilephone  from future.member order by id DESC limit 1'
                mobilephone = self.sql.do_sql(sql, 'one')['Mobilephone']
                if mobilephone == str(max_phone):
                    result = 'pass'
                else:
                    result = 'fail'
                    loger.get_log('info', '第{}条用例“{}”数据库较验出错'.format(case.case_id, case.title))
        except AssertionError as e:
            result = 'fail'
            loger.get_log('error', '第{}条用例“{}”出错{}'.format(case.case_id, case.title, e))
            raise e
        finally:
            loger.get_log('info', '********开始将结果写回excel数据********')
            self.t.write_data(sheet_name, int(case.case_id) + 1, 8, request_result)
            self.t.write_data(sheet_name, int(case.case_id) + 1, 9, result)
            loger.get_log('info', '********结束将结果写回excel数据********')

    @classmethod
    def tearDownClass(cls):
        cls.sql.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
