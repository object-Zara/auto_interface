# -*- coding:utf-8 -*-
# @datetime:2019/4/1 18:30
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:do_excel.py

from openpyxl import load_workbook
import json
from common import get_path


class DoExcelHttp:
    def __init__(self, file_name):
        self.file_name = file_name
        self.wb = load_workbook(file_name)

        # self.sheet = self.wb.worksheets[0]

    def get_init_data(self, sheet_name):
        """读取默认的手机号"""
        sheet = self.wb[sheet_name]
        mobile = sheet.cell(1, 2).value
        self.wb.close()
        return mobile

    def read_data(self, sheet_name):
        sheet = self.wb[sheet_name]
        list_data = []
        mobile = self.get_init_data('init')
        for row in range(2, sheet.max_row+1):
            dict_rowdata = {
                'case_id': sheet.cell(row, 1).value,
                'name': sheet.cell(row, 2).value,
                'method': sheet.cell(row, 3).value,
                'url': sheet.cell(row, 4).value,
                'expect': json.loads(sheet.cell(row, 6).value)
                # 'param': json.loads(sheet.cell(row, 5).value)
            }
            if sheet.cell(row, 5).value.find('${mobilephone}') != -1:  # find函数如果未找到会返回-1
                new_param = sheet.cell(row, 5).value.replace('${mobilephone}', str(mobile))
            else:
                new_param = sheet.cell(row, 5).value
            dict_rowdata['param'] = json.loads(new_param)
            list_data.append(dict_rowdata)
            # 更新手机号
            self.update_init_data('init', mobile+1)  # 通过在初始手机号上加1进行操作
        self.wb.close()
        return list_data

    def write_data(self, sheet_name, row, column, value):
        sheet = self.wb[sheet_name]
        sheet.cell(row, column, value)
        self.wb.save(self.file_name)
        self.wb.close()

    def update_init_data(self, sheet_name, value):
        self.write_data(sheet_name, 1, 2, value)


if __name__ == '__main__':
    doexcelhttp = DoExcelHttp(get_path.GetPath().get_test_case_path())
    print(doexcelhttp.read_data('register'))
