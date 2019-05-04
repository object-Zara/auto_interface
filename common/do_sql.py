# -*- coding:utf-8 -*-
""" 
@datetime:2019/4/21 16:15
@author:123
@email:1111@sina.com
@File:do_sql.py
@function： 获取数据库连接信息
"""
import pymysql
from common.read_config import ReadConfig


class DoSql:
    """通过switch开关及test和online文件的配置来确定sql"""
    def __init__(self):
        self.conf = ReadConfig('switch_sql', 'on')
        self.host = self.conf.get_contents('sql', 'host')
        self.user = self.conf.get_contents('sql', 'user')
        self.password = self.conf.get_contents('sql', 'password')
        self.port = self.conf.get_contents('sql', 'port')
        self.mysql = pymysql.connect(host=self.host, user=self.user, password=self.password, port=int(self.port))
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)  # 设置返回字典

    def do_sql(self, sql_query, result_type='one'):
        """
        :param str sql_query: sql执行语句
        :param str result_type: 查询结果值的数量
        返回查询结果
        """
        # 2,新建一个查询页面
        # 4，执行SQL
        self.cursor.execute(sql_query)
        self.mysql.commit()  # 更新执行结果
        # 5，查看结果
        if result_type == 'one':
            result = self.cursor.fetchone()  # 获取查询结果集里面最近的一条数据返回
        else:
            result = self.cursor.fetchall()  # 获取全部结果集
        return result

    def close(self):
        # 6，关闭查询
        self.cursor.close()
        # 7，关闭数据库连接
        self.mysql.close()


if __name__ == '__main__':
    conf_dosql = DoSql()
    # sql = 'SELECT MAX(Id) as ID from future.loan WHERE Status != 4'
    # print(conf_dosql.do_sql(sql, 'one'))

    # sql = 'select * from future.loan limit 3'
    # print(conf_dosql.do_sql(sql, 'all'))
    sql = 'select * from future.member where mobilephone =13777487502'
    print(conf_dosql.do_sql(sql, 'one'))
    # mobilephone = sql.do_sql(sql, 'one')['mobilephone']
    # print(mobilephone)
