# -*- coding:utf-8 -*-
# @datetime:2019/4/1 19:08
# @author:Xiaoyuan
# @email:Object_ycm@sina.com
# @File:logging_info.py

import logging.handlers
from common import get_path


class Mylogging:
    def __init__(self):
        # self.msg = config['level_msg']['msg']
        self.loger_name = 'loger'
        self.loger_level = 'INFO'
        self.handler_level = 'INFO'
        self.handler_out_filepath = get_path.GetPath().get_logging_path()
        self.encoding = 'utf-8'
        self.formt = logging.Formatter('%(asctime)s-%(filename)s-%(levelname)s-日志信息：%(message)s')

    def get_log(self, level, msg):
        try:
            logger = logging.getLogger(self.loger_name)
            handler = logging.handlers.TimedRotatingFileHandler(self.handler_out_filepath, when="midnight",
                                                                interval=1, backupCount=10, encoding="utf-8")
            logger.setLevel(self.loger_level)
            handler.setLevel(self.handler_level)

            handler.setFormatter(self.formt)

            logger.addHandler(handler)

            if level.upper() == 'DEBUG':
                logger.debug(msg)
            elif level.upper() == "INFO":
                logger.info(msg)
            elif level.upper() == 'WARNING':
                logger.warning(msg)
            elif level.upper() == 'ERROR':
                logger.error(msg)
            elif level.upper() == 'CRITICAL':
                logger.critical(msg)
            else:
                return '日志级别错误'
            logger.removeHandler(handler)
        except Exception as e:
            raise e
            return e


if __name__ == '__main__':
    mylog = Mylogging()
    mylog.get_log('error', '错误级别的日志')
