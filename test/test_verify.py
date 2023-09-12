# coding : utf-8
from core.handler.validator import *


def test1():
    # 测试本机IP
    getMyIp()


def test2():
    # 测试源IP是不是代理IP
    proxy = 'http://8.210.37.63:59394'
    proxies = {"http": proxy, "https": proxy}
    getMyIp(proxies=proxies)


def test3():
    # 测试IP是否有效，并返回响应速度
    proxy = 'http://8.210.37.63:59394'
    single_validator_http_https(you_proxy=proxy)


if __name__ == '__main__':
    # test1()
    # test2()
    test3()
