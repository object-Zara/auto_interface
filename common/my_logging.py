# -*- coding:utf-8 -*-
# @datetime:2019/4/1 19:08
# @author:123
# @email:1111@sina.com
# @File:logging_info.py

import logging.handlers
import os
from common import get_path
import datetime
from configparser import ConfigParser


class Mylogging:
    def __init__(self):
        self.config = ConfigParser()
        logging_conf_path = get_path.GetPath().get_conf_logging_path()
        self.config.read(logging_conf_path, encoding='utf-8')
        self.loger_name = self.config.get('logger_name', 'name')
        self.loger_level = self.config.get('logger_name', 'level')
        self.handler_level = self.config.get('file_handler', 'level')
        self.handler_out_filepath = get_path.GetPath().get_logging_path()
        self.encoding = self.config.get('encode', 'encoding')
        self.formt = logging.Formatter(self.config.get('formatter', 'format'))

    def get_log(self, level, msg):
        try:
            logger = logging.getLogger(self.loger_name)
            logger_file_name = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
            logger_file_path = os.path.join(self.handler_out_filepath, logger_file_name)
            handler = logging.handlers.TimedRotatingFileHandler(logger_file_path, when="midnight",
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
