# -*- coding:utf-8 -*-
""" 
@datetime:2019/5/4 0:24
@author:123
@email:1111@sina.com
@File:test_connect_invest.py 
@function： 熟悉接口间的关联
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
sheet_name = 'connect_invest'
data_doexcel = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path()).read_data(sheet_name)


@ddt
class TestConnectInvest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loger = my_logging.Mylogging()
        cls.http_request = http_request.MyRequest()
        cls.t = do_excel.DoExcelHttp(get_path.GetPath().get_test_case_data_path())
        cls.sql = do_sql.DoSql()

    @data(*data_doexcel)
    def test_connect_invest(self, case):
        """对/member/bidLoan接口请求关联测试"""
        if case.case_excute.upper() == "NO":
            self.skipTest('该条用例不执行')
        self.loger.get_log('info', '************************************')
        self.loger.get_log('info', '正在执行第{}条用例“{}”'.format(case.case_id, case.title))

        case.data = json.loads(do_re.do_re(case.data, 'user_data', pattern="#(.*?)#"))
        request_result = self.http_request.request(case.method, case.url, data=case.data)
        try:
            self.assertEqual(str(case.expect), json.loads(request_result.text)["code"])
            testresult = 'pass'
            # 判断加标成功之后，查询数据库，取到loan_id
            if request_result.json()['msg'] == "加标成功":
                sql = "select id from future.loan where memberid = 97 order by id desc limit 1"
                loan_id = self.sql.do_sql(sql, 'one')['id']
                setattr(do_re.Context, "bidloan_id", str(loan_id))
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
