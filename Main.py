# coding : utf-8
from core.db.Sqlite3Impl import Sqlite
from core.handler.crawlStie import crawl
from core.handler.output import ToExcel
from core.handler.validator import verified


def crawl_website():
    data = crawl.start()
    for i in data:
        insert_time = i[0]
        ip = i[1]
        port = i[2]
        area = i[3]
        country = i[4]
        proxy_type = i[5]
        # print(insert_time, ip, port, area, country, proxy_type)
        Sqlite.insert(table='proxy_ip', param=[insert_time, ip, port, area, country, proxy_type, '', '', ''])
    verify = verified()
    return data, verify


def main():
    columns1 = ['时间', 'IP', '端口', '位置', '国家', '代理类型']
    columns2 = ['IP', '端口', '位置', '国家', '代理类型', '支持的协议', '响应速度', '验证时间', '代理链接']
    content = crawl_website()
    data1 = content[0]
    data2 = content[1]
    path1 = ".\\未验证的代理.xlsx"
    path2 = ".\\验证后的代理.xlsx"
    ToExcel(columns=columns1, data=data1, path=path1).output()
    ToExcel(columns=columns2, data=data2, path=path2).output()


if __name__ == '__main__':
    main()
    # crawl_website()
