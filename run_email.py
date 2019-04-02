# -*- coding:utf-8 -*-
# @datetime:2019/4/2 10:47
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:run_email.py.py
import os
from common import send_email
from common import get_path


def bat_send_email():
    report_path = get_path.GetPath().get_email_report_path()
    lists = os.listdir(report_path)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(report_path + "\\" + fn))  # 按时间排序
    file_new = os.path.join(report_path, lists[-1])  # 获取最新的文件保存到file_new

    smail = send_email.SendEMail()
    smail.add_content('html', file_new, lists[-1])
    smail.send_email('彩', '测试报告', '接口测试报告')


if __name__ == '__main__':
    bat_send_email()
