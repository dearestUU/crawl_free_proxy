# coding : utf-8
import datetime
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import Union
from core import logger
from core.db.Sqlite3Impl import Sqlite
from core.handler.userAgent import get_1_random_ua
from core.setting import TEST_URL, MAX_THREAD

import warnings
warnings.filterwarnings('ignore')


def getMyIp(proxies: dict = None):
    """
    :param proxies: 传入一个字典 {"http":"http://xxx.xxx.xxx.xxx:xx","https":"http://xxx.xxx.xxx.xxx:xx"}
    :return: 获取出网后的地址
    """
    check_url = TEST_URL
    headers = {"User-Agent": get_1_random_ua()}

    try:
        if proxies is None:
            resp = requests.get(url=check_url, headers=headers, timeout=5)
        else:
            resp = requests.get(url=check_url, headers=headers, proxies=proxies, timeout=5)
        result = resp.json()['origin']
    except Exception as ex:
        logger.error(msg=f"Error in get IP address! reason: {ex}")
    else:
        logger.info(msg=f"Your IP: {result}")


def single_validator_http_https(you_proxy: str) -> Union[str, None, tuple]:
    """
    :param you_proxy: 传入你的http/https代理地址
    :return: 验证 HTTP代理 是否有效. 返回一个元组 "http",http_proxy
    """

    if you_proxy.startswith('https://') or you_proxy.startswith('http://'):
        pass
    else:
        logger.error(msg=f"Not start with `http` or `https` protocol -> {you_proxy}")
        return

    protocol_ip_port = you_proxy.split('://')
    support_protocol = protocol_ip_port[0]  # 支持的协议类型
    ip_port = protocol_ip_port[1].split(':')
    ip = ip_port[0]
    port = ip_port[1]

    check_url = TEST_URL  # 测试代理是否匿名、高匿、透明
    check_proxy = {"http": you_proxy, "https": you_proxy}
    headers = {"User-Agent": get_1_random_ua()}
    try:
        sTime = time.time()
        resp = requests.get(url=check_url, headers=headers, proxies=check_proxy, timeout=5)
        if resp.ok:
            validate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M%S')  # 验证时间
            response_speed = round(time.time() - sTime, 2)  # 响应速度
            result = resp.json()
            originIP = result['origin']  # 获取测试网站返回的 origin IP
            if ip == originIP:
                """如果origin和代理IP相等，说明是匿名或者高匿代理"""
                header = result['headers']  # 获取测试网站返回的 headers
                if 'Proxy-Connection' in header:
                    proxy_type = '透明'  # 代理类型
                else:
                    if 'X-Forwarded-For' in header and header['X-Forwarded-For'] == ip:
                        proxy_type = '匿名'
                    elif 'X-Forwarded-For' in header and header['X-Forwarded-For'] != ip:
                        proxy_type = '透明'
                    else:
                        proxy_type = '高匿'
                logger.info(msg=f"Congratulations! Your Proxy: {you_proxy}  | Response Speed: {response_speed} sec.")
                return you_proxy, proxy_type, support_protocol, response_speed, validate_time
            else:
                """说明代理无效"""
                logger.error(f"Invalid Proxy! -> {you_proxy}")
                return None
        else:
            raise Exception
    except Exception as ex:
        logger.warning(msg=f"Invalid HTTP or HTTPS -> {you_proxy} . reason : {ex}")
        return None


def batch_validator_http_https(proxyList: list):
    """
    :param proxyList: 传入一个列表
    :return: 批量验证 HTTP/HTTPS 代理是否有效
    """

    result = []
    with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
        future = [executor.submit(single_validator_http_https, proxy) for proxy in proxyList]
        for f in future:
            ff = f.result()
            if ff is not None:
                result.append(ff)
    return result


def check_validator_batch(fieldList: list):
    """
    :param fieldList: 传入一个列表
    :return: 批量验证 HTTP/HTTPS 代理是否有效
    """
    result = []
    with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
        future = [executor.submit(check_validator_single, field) for field in fieldList]
        for f in future:
            ff = f.result()
            if ff is not None:
                result.append(ff)
    return result


def check_validator_single(fields: str):
    """
    :param fields: 没有验证的字段，需传入一个 元组（包含 proxy, ip,port,area,country） 类似 f"http://{ip}:{port}||{area}||{country}"
    :return: 自己的逻辑，并不通用
    """
    field = fields.split('||')
    proxy_link = field[0].strip('/')  # 代理链接
    area = field[1]  # 区域
    country = field[2]  # 国家
    protocol_ip_port = proxy_link.split('://')
    support_protocol = protocol_ip_port[0]  # 支持的协议
    ip_port = protocol_ip_port[1].split(':')
    ip = ip_port[0]  # ip
    port = ip_port[1]  # 端口

    check_url = TEST_URL  # 测试代理是否匿名、高匿、透明
    check_proxy = {"http": proxy_link, "https": proxy_link}
    headers = {"User-Agent": get_1_random_ua()}

    try:
        sTime = time.time()
        resp = requests.get(url=check_url, headers=headers, proxies=check_proxy, timeout=5)
        if resp.ok:
            validate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 验证时间
            response_speed = round(time.time() - sTime, 2)  # 响应速度
            result = resp.json()
            originIP = result['origin']  # 获取测试网站返回的 origin IP
            if ip == originIP:
                """如果origin和代理IP相等，说明是匿名或者高匿代理"""
                header = result['headers']  # 获取测试网站返回的 headers
                if 'Proxy-Connection' in header:
                    proxy_type = '透明'  # 代理类型
                else:
                    if 'X-Forwarded-For' in header and header['X-Forwarded-For'] == ip:
                        proxy_type = '匿名'
                    elif 'X-Forwarded-For' in header and header['X-Forwarded-For'] != ip:
                        proxy_type = '透明'
                    else:
                        proxy_type = '高匿'
                logger.info(msg=f"Congratulations! Your Proxy: {proxy_link}  | Response Speed: {response_speed} sec.")
                return ip, int(
                    port), area, country, proxy_type, support_protocol, f'{response_speed}秒', validate_time, proxy_link
            else:
                """说明代理无效"""
                logger.error(f"Invalid Proxy! -> {proxy_link}")
                return None
        else:
            raise Exception
    except Exception as ex:
        # logger.warning(msg=f"Invalid HTTP or HTTPS -> {proxy_link} . reason : {ex}")
        logger.warning(msg=f"Invalid HTTP or HTTPS -> {proxy_link}")
        return None


def verified() -> list:
    verify = Sqlite.select(sql='select * from proxy_ip', value=()).fetchall()  # 从proxy_ip中获取
    verified_list = []
    for i in verify:
        ip = i[1]
        port = i[2]
        area = i[3]
        country = i[4]
        field1 = f"http://{ip}:{port}||{area}||{country}"
        field2 = f"https://{ip}:{port}||{area}||{country}"
        verified_list.append(field1)
        verified_list.append(field2)
    paramList = check_validator_batch(fieldList=verified_list)
    [Sqlite.insert(table='verified_proxy', param=param) for param in paramList]  # 插入 verified_proxy中
    return paramList

