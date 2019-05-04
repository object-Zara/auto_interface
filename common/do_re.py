# -*- coding:utf-8 -*-
""" 
@datetime:2019/4/21 17:21
@author:123
@email:1111@sina.com
@File:do_re.py 
@function： 用正则方式处理用例中的参数
"""
import re
from configparser import NoOptionError
from common.read_config import ReadConfig


class Context:
    bidloan_id = 'aa'


def do_re(data, section, pattern="#(.*?)#"):
    while re.search(pattern, data):
        match_data = re.search(pattern, data)
        param_key = match_data.group(1)  # 拿到参数化的KEY
        try:
            param_value = ReadConfig('switch_data', 'on').get_contents(section, param_key)
        except Exception as e:  # 如果配置文件里面没有的时候，去Context里面取
            if hasattr(Context, param_key):
                param_value = getattr(Context, param_key)
            else:
                print('找不到参数化的值')
                raise e
        # 记得替换后的内容，继续用data接收
        data = re.sub(pattern, param_value, data, count=1)  # 查找替换,count查找替换的次数
    return data


if __name__ == '__main__':
    data_sql = '{"loanId": "#bidloan_id#"}'
    res = do_re(data_sql, 'user_data', pattern="#(.*?)#")
    print(res)
