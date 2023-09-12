# coding : utf-8
import os

import pandas as pd
from datetime import datetime
from core import logger


class ToExcel:
    def __init__(self, columns: list, data, path, num: int = 1):
        """
        :param num: 传入的编号1 表示生成不重复的数据，其他数字表示重复。默认生成不重复的数据
        :param columns: 列名
        :param data: 数据，可以是list格式的，但要对齐工整
        :param path: 输出的路径
        """
        self.num = num
        self.columns = columns
        self.data = data
        self.path = path
        self.xlsxName = os.path.basename(path)
        self.xlsxPath = os.path.dirname(path)

    def output(self):
        """
        :return: 用于生成不重复的
        """
        if self.xlsxName not in os.listdir(path=self.xlsxPath):
            try:
                df = pd.DataFrame(data=self.data, columns=self.columns)
                if self.num == 1:
                    df.drop_duplicates(inplace=True)
                with pd.ExcelWriter(path=self.path, engine='openpyxl') as write:
                    df.to_excel(write, index=False)
                logger.info(f">>> `{self.xlsxName}` 表格在路径中: `{self.xlsxPath}`")
            except Exception as ex:
                logger.error(msg=f">>> {self.path} 表格写入有问题: {ex}")
        else:
            try:
                df1 = pd.DataFrame(data=self.data, columns=self.columns)
                df1.apply(pd.to_numeric, errors='ignore')  # 数据类型转换
                df2 = pd.read_excel(self.path, engine='openpyxl', )  # 读取表格中的源数据
                df2.apply(pd.to_numeric, errors='ignore')  # 数据类型转换
                df = pd.concat([df1, df2], axis=0, ignore_index=True)  # 先合并，在写入
                if self.num == 1:
                    df.drop_duplicates(inplace=True, keep='first')
                try:
                    with pd.ExcelWriter(path=self.path, engine='openpyxl', mode='a',
                                        if_sheet_exists='replace') as writer:
                        df.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
                    logger.info(f">>> `{self.xlsxName}` 表格在路径中: `{self.xlsxPath}`")
                except PermissionError:
                    logger.info(">>> 由于表格被另一程序占用，正在重新生成表格...")
                    xlsxName1 = f"result{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"  # 新表格名称
                    path1 = os.path.join(self.xlsxPath, xlsxName1)  # 新的表格路径
                    with pd.ExcelWriter(path=path1, engine='openpyxl') as write:
                        df.to_excel(write, index=False)
                    logger.info(f">>> `{xlsxName1}` 表格在路径中: `{self.xlsxPath}`")
            except Exception as ex:
                logger.error(msg=f">>> {self.path} 表格写入有问题: {ex}")
