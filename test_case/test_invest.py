# -*- coding:utf-8 -*-
""" 
@datetime:2019/4/21 21:18
@author:123
@email:1111@sina.com
@File:tes_invest.py 
@function：对投资接口的测试
"""
import json
import unittest
from ddt import ddt, data
from common import http_request
from common import do_excel
from common import my_logging
from common import get_path
from common import do_sql
from common import do_re

"""从excel读取数据"""
sheet_name = 'invest'
data_doexcel = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path()).read_data(sheet_name)


@ddt
class TestInvest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loger = my_logging.Mylogging()
        cls.http_request = http_request.MyRequest()
        cls.t = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path())
        cls.sql = do_sql.DoSql()

    @data(*data_doexcel)
    def test_invest(self, case):
        """对/member/bidLoan接口请求的测试"""
        if case.case_excute.upper() == "NO":
            self.skipTest('该条用例不执行')
        self.loger.get_log('info', '************************************')
        self.loger.get_log('info', '正在执行第{}条用例“{}”'.format(case.case_id, case.title))

        case.data = json.loads(do_re.do_re(case.data, 'user_data', pattern="#(.*?)#"))
        if 'memberId' in case.data.keys():
            int(case.data['memberId'])
            int(case.data['loanId'])

        elif case.title == '用户不存在':
            sql = 'select max(id) from future.member'
            member_id = self.sql.do_sql(sql, 'one')['max(id)']
            # 最大MemberID+1
            max_id = int(member_id) + 1
            # replace方法是特换之后重新返回一个新的字符串，所以需要使用case.data重新接收
            case.data['memberId'] = max_id  # 替换参数值

        elif case.title == '标不存在':
            sql = 'SELECT MAX(id) from future.loan'
            loan_id = self.sql.do_sql(sql, 'one')['MAX(id)']
            max_id = loan_id + 1
            case.data['loanId'] = max_id  # 替换参数值

        elif case.title == '对满标的标投资':
            sql = 'SELECT MAX(id) from future.loan WHERE FullTime IS NOT NULL'
            loan_id = self.sql.do_sql(sql, 'one')['MAX(id)']
            case.data['loanId'] = loan_id  # 替换参数值

        elif case.title == '对不在竞标状态的标投资':
            sql = 'SELECT MAX(Id) from future.loan WHERE Status != 4'
            loan_id = self.sql.do_sql(sql, 'one')['MAX(Id)']
            case.data['loanId'] = loan_id   # 替换参数值

        elif case.title == '用户余额不足':
            sql = 'select MAX(Id) from future.member WHERE LeaveAmount=0'
            member_id = self.sql.do_sql(sql, 'one')['MAX(Id)']
            case.data['memberId'] = member_id  # 替换参数值
            sql = 'select min(id) from future.loan WHERE `Status`=4'
            loan_id = self.sql.do_sql(sql, 'one')['min(id)']
            case.data['loanId'] = loan_id  # 替换参数值

        request_result = self.http_request.request(case.method, case.url, data=case.data)
        try:
            self.assertEqual(str(case.expect), json.loads(request_result.text)["code"])
            testresult = 'pass'
        except AssertionError as e:
            testresult = 'failed'
            self.loger.get_log('error', '第{}条用例“{}”出错{}'.format(case.case_id, case.title, e))
            raise e
        finally:
            self.loger.get_log('info', '********开始将结果写回excel数据********')
            self.t.write_data(sheet_name, int(case.case_id) + 1, 8, request_result.text)
            self.t.write_data(sheet_name, int(case.case_id)+1, 9, testresult)
            self.loger.get_log('info', '********结束将结果写回excel数据********')

    @classmethod
    def tearDownClass(cls):
        cls.sql.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)

