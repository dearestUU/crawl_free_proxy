# _*_ coding:utf-8 _*_
"""
-------------------------------------------------------------------------------------------
@Author: dearest
@Data: 2023/08/19 12:00:00
@File: __init__.py
@Version: 1.0.0
@Description:
-------------------------------------------------------------------------------------------
"""

__title__ = ""
__version__ = ""
__author__ = 'YY_dearest'

import time
from core.handler.log import LOGGER,LOGGER_R

logger = LOGGER
logger_r = LOGGER_R()

def coast_time(func):
    def wrapper(*args, **kwargs):
        sTime = time.time()
        result = func(*args, **kwargs)
        eTime = time.time()
        logger.info(f">>> run function {func.__name__} coast {(eTime - sTime):6f} seconds.")
        return result

    return wrapper

