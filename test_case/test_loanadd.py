# -*- coding:utf-8 -*-
""" 
@datetime:2019/4/21 19:15
@author:123
@email:1111@sina.com
@File:test_loanadd.py 
@function： 新增项目接口的用例
"""
import json
import unittest
from ddt import ddt, data
from common import http_request
from common import do_excel
from common import my_logging
from common import get_path
from common import do_re
from common import do_sql

"""从excel读取数据"""
sheet_name = 'loan_add'
data_doexcel = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path()).read_data(sheet_name)
loger = my_logging.Mylogging()


@ddt
class TestLoanAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http_request = http_request.MyRequest()
        cls.t = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path())
        cls.sql = do_sql.DoSql()

    @data(*data_doexcel)
    def test_loanadd(self, case):
        """对/loan/add接口请求的测试"""
        if case.case_excute.upper() == "NO":
            self.skipTest('该条用例不执行')
        loger.get_log('info', '************************************')
        loger.get_log('info', '正在执行第{}条用例“{}”'.format(case.case_id, case.title))
        if case.title == '未注册的用户加标':
            sql = 'select max(id) from future.member'
            member_id = self.sql.do_sql(sql, 'one')['max(id)']
            # 最大手机号码+1
            max_id = int(member_id) + 1
            # replace方法是特换之后重新返回一个新的字符串，所以需要使用case.data重新接收
            case.data = case.data.replace('#loan_member_id#', str(max_id))  # 替换参数值
        else:
            case.data = do_re.do_re(case.data, 'user_data', pattern="#(.*?)#")
        loger.get_log('info', '请求的参数为：{},{}'.format(case.url, case.data))
        request_result = self.http_request.request(case.method, case.url, data=case.data)
        try:
            self.assertEqual(str(case.expect), json.loads(request_result.text)["code"])
            testresult = 'pass'
        except AssertionError as e:
            testresult = 'failed'
            loger.get_log('error', '第{}条用例“{}”出错{}'.format(case.case_id, case.title, e))
            raise e
        finally:
            loger.get_log('info', '********开始将结果写回excel数据********')
            self.t.write_data(sheet_name, int(case.case_id) + 1, 8, request_result.text)
            self.t.write_data(sheet_name, int(case.case_id)+1, 9, testresult)
            loger.get_log('info', '********结束将结果写回excel数据********')

    @classmethod
    def tearDownClass(cls):
        cls.sql.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)


