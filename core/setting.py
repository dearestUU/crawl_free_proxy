# _*_ coding:utf-8 _*_
"""
-------------------------------------------------------------------------------------------
@Author: dearest
@Data: 2023/08/19 12:00:00
@File: setting.py
@Version: 1.0.0
@Description: 程序配置文件
-------------------------------------------------------------------------------------------
"""

import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))  # 当前setting.py文件的路径

MAX_PAGE = 20  # 爬取网站多少页

SQLITE3_PATH = os.path.join(CURRENT_PATH, 'db', 'ProxyIp.db')

TEST_URL = 'http://httpbin.org/get'  # 测试代理是否有效的URL

AIOHTTP_LIMIT = 25  # limit默认100，limit=0的时候是无限制,表示同一时间连接的http数量
AIOHtTP_LIMIT_PER_PORT = 5  # limit_per_host,同一端口连接数量.
AIOHTTP_SEM = 5  # aiohttp的信标设置，表示多少次并发。必须是数字。默认是5，建议 limit_per_host * sem = limit
AIOHTTP_URL_COUNT = 50  # 每次aiohttp请求的url个数
MAX_THREAD = 200  # 解析html时最大的线程数量
