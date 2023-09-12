# coding : utf-8
from core.handler.crawlStie import crawl
from core.handler.output import ToExcel


def test1():
    # 测试拉取数据
    crawl.start()


def test2():
    # 测试拉取到数据后写入表格
    data = crawl.start()
    path = '.\\xlsx.xlsx'
    ToExcel(columns=['插入时间', 'IP', '端口', '位置', '国家', '代理类型'], data=data, path=path).output()
    print(f'表格已导出在 {path} 表格!')


if __name__ == '__main__':
    test1()
