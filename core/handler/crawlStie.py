# coding : utf-8
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from core.handler.requestByAiohttp import T
from core.setting import MAX_THREAD, MAX_PAGE

CHINA_AREA = [
    '河北', '山东', '辽宁', '黑龙江', '吉林',
    '甘肃', '青海', '河南', '江苏', '湖北',
    '江西', '浙江', '广东', '云南', '福建',
    '台湾', '海南', '山西', '四川', '陕西',
    '贵州', '安徽', '重庆', '北京', '上海',
    '天津', '广西', '内蒙', '西藏', '新疆',
    '宁夏', '香港', '澳门', '湖南']


def _parse_website1(resp_html) -> list:
    """
    :param resp_html: http://www.66ip.cn/ 网站返回的html
    :return: 返回解析后的 ip , port , proxy_location , proxy_type , first_validation_time
    """
    # resp_html = resp_html.decode('gbk')
    data_list = []
    soup = BeautifulSoup(resp_html, features='html.parser')
    table = soup.find(name='table', attrs={"width": "100%", "border": "2px"})  # 找到table
    tmp_tmp = []
    for row in table.find_all('tr'):  # 找出所有的tr

        columns = row.find_all('td')
        ip = columns[0].text
        port = columns[1].text
        proxy_location = columns[2].text
        proxy_type = columns[3].text.replace('代理', '')
        insert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        area = ''
        for _ in CHINA_AREA:
            if _ in proxy_location:
                area = '中国'
            else:
                pass

        if area == '中国':
            country = '中国'
        else:
            country = '非中国'

        first_validation_time = columns[4].text

        if ip == 'ip' and port == '端口号' and proxy_location == '代理位置' and proxy_type == '类型' and first_validation_time == '验证时间':
            pass
        else:
            ip_port = f"{ip}-{port}"
            if ip_port not in tmp_tmp:
                # print(insert_time, ip, int(port), proxy_location, country, proxy_type)
                data_list.append([insert_time, ip, int(port), proxy_location, country, proxy_type])
                tmp_tmp.append(ip_port)
            else:
                pass

    return data_list


def parse_website2(resp_html) -> list:
    """
    :param resp_html: https://www.kuaidaili.com 网站返回的html
    :return: 返回 IP	  PORT	匿名度	类型	  get/post支持	位置	响应速度	最后验证时间
    """
    data_list = []
    soup = BeautifulSoup(resp_html, features='html.parser')
    tbody_label = soup.find(name='div', attrs={"class": "section stat", "id": "freeList"})
    for row in tbody_label.find_all('tr'):  # 找出所有的tr
        columns = row.find_all('td')
        if len(columns) != 8:
            pass
        else:
            ip = columns[0].text
            port = columns[1].text
            proxy_type = columns[2].text.replace('高匿名', '高匿')
            support_type = columns[3].text
            http_method = columns[4].text
            proxy_location = columns[5].text
            response_speed = columns[6].text
            last_verify_time = columns[7].text
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:00')
            data_list.append([ip, port, proxy_location, proxy_type])
            # data_list.append([ip,port,proxy_type,support_type,http_method,proxy_location,response_speed,last_verify_time,now_time])
            # print(ip,port,proxy_type,support_type,http_method,proxy_location,response_speed,last_verify_time,now_time)
    return data_list


def parse_website3(resp_html) -> list:
    """
    :param resp_html: https://www.kuaidaili.com 网站返回的html
    :return: IP	PORT	匿名度	类型	位置	响应速度	最后验证时间	付费方式
    """
    data_list = []
    soup = BeautifulSoup(resp_html, features='html.parser')
    tbody_label = soup.find(name='tbody')
    for row in tbody_label.find_all('tr'):  # 找出所有的tr
        columns = row.find_all('td')
        if len(columns) != 8:
            pass
        else:
            ip = columns[0].text
            port = columns[1].text
            proxy_type = columns[2].text.replace('高匿名', '高匿')
            support_type = columns[3].text
            proxy_location = columns[4].text
            response_speed = columns[5].text
            last_verify_time = columns[6].text
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:00')
            data_list.append([ip, port, proxy_location, proxy_type])
            # print(ip, port, proxy_location, proxy_type)
    return data_list


class crawl:
    name = "爬取特定的几个代理网站"

    # @staticmethod
    # def website1() -> list:
    #     """
    #     :return: 爬取 http://www.66ip.cn 这个网站的 全国代理。只爬取近期有效的，如果爬取全部，请修改如下代码
    #     """
    #     website1_result = []
    #
    #     """
    #     # 如果爬取全部，就把这段代码的注释取消，然后把下面 maxPage = 15 注释掉
    #     url = 'http://www.66ip.cn'
    #     resp_html = requests.get(url=url).content.decode('gbk', 'ignore')
    #     a_label = BeautifulSoup(resp_html, features='html.parser').find(name='div',attrs={"id": "PageList"})
    #     maxPage = []  # index页面的最大数量，只爬近期有效的，而不是都爬下来
    #     [maxPage.append(int(_.text)) for _ in a_label.find_all('a') if _.text.isdigit()]
    #     maxPage = max(maxPage)
    #     """
    #     maxPage = 15
    #     urlList = ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(2, maxPage))]
    #     with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
    #         future = [executor.submit(parse_website1, html[0]) for html in T.T_MAIN(urlList=urlList)]
    #         for f in future:
    #             website1_result += f.result()
    #     return website1_result
    #
    # @staticmethod
    # def website2() -> list:
    #     """
    #     :return: 爬取 http://www.66ip.cn 这个网站的省市级代理.只爬取近期有效的
    #     """
    #     website1_result = []
    #     urlList = ['http://www.66ip.cn/areaindex_%s/%s.html' % (m, n) for m in range(1, 34) for n in range(1, 10)]
    #     with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
    #         future = [executor.submit(parse_website1, html[0]) for html in T.T_MAIN(urlList=urlList)]
    #         for f in future:
    #             website1_result += f.result()
    #     return website1_result

    @staticmethod
    def _website(urlList: list, parse_method) -> list:
        result = []
        with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
            future = [executor.submit(parse_method, html[0]) for html in T.T_MAIN(urlList=urlList)]
            for f in future:
                result += f.result()
        df = pd.DataFrame(data=result)
        df = df.drop_duplicates()
        return df.values.tolist()

    @staticmethod
    def start() -> list:
        """
        :return: 目前只支持爬取 http://www.66ip.cn 这一个站点的免费代理
        """
        urls1 = ['http://www.66ip.cn/areaindex_%s/%s.html' % (m, n) for m in range(1, 34) for n in
                 range(1, 10)]  # 近期省市级代理
        urls2 = ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(2, MAX_PAGE))]  # 近期全国代理
        urls = urls1 + urls2
        return crawl._website(urlList=urls, parse_method=_parse_website1)

    # @staticmethod
    # def go1() -> list:
    #     """
    #     :return: http://www.kuaidaili.com 这个网站有防止爬虫限制
    #     """
    #     urls1 = ['https://www.kuaidaili.com/ops/proxylist/%s/#freeList' % n for n in range(1, 11)]  # 这个网站的代理.100个免费的代理
    #     urls2 = ['http://www.kuaidaili.com/free/%s/%s/' % (m, n) for m in ['inha', 'intr'] for n in range(1, 11)]  # 爬取这个网站 国内高匿和普通代理
    #     res1 = Crawl.website(urlList=urls1, parse_method=parse_website2)
    #     res2 = Crawl.website(urlList=urls2, parse_method=parse_website3)
    #     return res1 + res2
