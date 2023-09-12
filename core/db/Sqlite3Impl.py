# coding : utf-8
import sqlite3
from sqlite3 import Cursor

from core import logger
from core.setting import SQLITE3_PATH


class Sqlite:
    name = "插入sqlite3中.数据在 ProxyIp.proxy_ip中."
    connection = sqlite3.connect(SQLITE3_PATH)

    @classmethod
    def delete(cls, ip, table: str, port: int = None, protocol=None):
        """
        :param table: 必须指定数据库中的表格
        :param ip:
        :param port:
        :param protocol:
        :return: 删除成功返回True,失败返回False
        """
        if table == 'proxy_ip' or table == 'verified_proxy':  # 必须指定表格名称
            if port is not None and protocol is not None:
                sql = f"delete from `{table}` where ip = ? and port = ? and support_protocol = ?"
                value = (ip, port, protocol)
                isSuccess = cls.is_exists(ip=ip, port=port, protocol=protocol, table=table)
                say1 = f'Table: {table} -> `{ip}:{port}` of `{protocol}` has deleted!'
                say2 = f'Table: {table} -> `{ip}:{port}` of `{protocol}` delete failed!'
                say3 = f'Table: {table} -> `{ip}:{port}` of `{protocol}` not exists.'
            elif protocol is None and port is not None:
                sql = f"delete from `{table}` where ip = ? and port = ?"
                value = (ip, port,)
                isSuccess = cls.is_exists(ip=ip, port=port, protocol=protocol,table=table)
                say1 = f'Table: {table} -> `{ip}:{port}` has deleted!'
                say2 = f'Table: {table} -> `{ip}:{port}` delete failed!'
                say3 = f'Table: {table} -> `{ip}:{port}` not exists.'
            else:
                sql = f"delete from `{table}` where ip = ?"
                value = (ip,)
                isSuccess = cls.is_exists(ip=ip, port=port, protocol=protocol, table=table)
                say1 = f'Table: {table} -> `{ip}` has deleted!'
                say2 = f'Table: {table} -> `{ip}` delete failed!'
                say3 = f'Table: {table} -> `{ip}` not exists.'

            if isSuccess:
                if cls.execute_update(sql=sql, value=value):
                    logger.info(msg=say1)
                else:
                    logger.error(msg=say2)
            else:
                logger.info(msg=say3)
        else:
            logger.error(msg='you input table name is wrong. must declare which TABLE in sqlite3! ')

    @classmethod
    def execute_select(cls, sql, value) -> Cursor:
        """
        :param sql: 待执行的 查询sql语句.
        :param value:
        :return:
        """
        try:
            with cls.connection as conn:
                cursor = conn.cursor()
                cursor.execute(sql, value)
        except Exception as ex:
            logger.error(f'>>> execute SELECT statement: `{sql}` failed. reason: {ex}')
        else:
            return cursor

    @classmethod
    def execute_update(cls, sql, value: tuple) -> bool:
        """
        :param sql: 待执行的 增删改sql语句.
        :param value: 传入的参数，必须是元组的形式
        :return: 执行成功返回 True, 失败返回 False
        """
        try:
            with cls.connection as conn:
                conn.cursor().execute(sql, value)
        except Exception as ex:
            logger.error(f'>>> execute statement: `{sql}` failed. reason: {ex}')
            return False
        else:
            # logger.info(f'>>> execute statement: `{sql}` success.')
            return True

    @classmethod
    def update(cls, param: list, table: str):
        if table == 'verified_proxy':
            sql = f"update `{table}` set area = ?, country = ?, proxy_type = ?, support_protocol = ?, response_speed = ?, validate_time = ?,proxy_link = ? where ip = ? and port = ?"
            value = (param[2], param[3], param[4], param[5], param[6], param[7], param[8], param[0], param[1])
            if cls.execute_update(sql=sql, value=value):
                logger.info(msg=f">>> `{param[0]}:{param[1]}` of `{param[5]}` update verified_proxy table success!")
            else:
                logger.error(msg=f">>> `{param[0]}:{param[1]}` of `{param[5]}` update verified_proxy table failed!")
        elif table == 'proxy_ip':
            sql = f"update `{table}` set insert_time = ?, area = ?, country = ?, proxy_type = ?, support_protocol = ?, response_speed = ?, validate_time = ? where ip = ? and port = ?"
            value = (param[0], param[3], param[4], param[5], param[6], param[7], param[8], param[1], param[2])
            if cls.execute_update(sql=sql, value=value):
                logger.info(msg=f">>> `{param[1]}:{param[2]}` of `{param[6]}` update proxy_ip table success.")
            else:
                logger.error(msg=f">>> `{param[1]}:{param[2]}` of `{param[6]}` update proxy_ip table failed!")
        else:
            logger.error("No such Table.")

    @classmethod
    def insert(cls, param: list, table: str):
        """
        :param table: 必须指定数据库中 表名
        :param param: 一条一条插入  proxy_ip 这个表中
        :return:
        """

        if table == 'proxy_ip' or table == 'verified_proxy':
            sql = f"insert into `{table}` values (?,?,?,?,?,?,?,?,?)"
            value = (param[0], param[1], param[2], param[3], param[4], param[5], param[6], param[7], param[8])
        else:
            logger.error(f'>>> you input Table Name is wrong!')
            return
        try:
            if table == 'proxy_ip':
                if cls.is_exists(ip=param[1], port=param[2], protocol=param[6], table=table):
                    # logger.info(msg=f'>>> `{param[1]}:{param[2]}` of `{param[6]}` has exists.')
                    cls.update(param=param, table='proxy_ip')  # 如果存在表中，就更新
                else:
                    if cls.execute_update(sql=sql, value=value):
                        logger.info(msg=f">>> `{param[1]}:{param[2]}` of `{param[6]}` insert proxy_ip table success.")
                    else:
                        logger.error(msg=f">>> `{param[1]}:{param[2]}` of `{param[6]}` insert proxy_ip table failed!")
            elif table == 'verified_proxy':
                if cls.is_exists(ip=param[0], port=param[1], protocol=param[5], table=table):
                    # logger.info(msg=f'>>> `{param[0]}:{param[1]}` of `{param[5]}` has exists.')
                    cls.update(param=param, table='verified_proxy')  # 如果之前验证过，就更新
                else:
                    if cls.execute_update(sql=sql, value=value):
                        logger.info(msg=f">>> `{param[0]}:{param[1]}` of `{param[5]}` insert verified_proxy table success.")
                    else:
                        logger.error(msg=f">>> `{param[0]}:{param[1]}` of `{param[5]}` insert verified_proxy table failed!")
            else:
                logger.error("No such Table.")
        except Exception as ex:
            logger.error(f"insert table failed, reason: {ex}")

    @classmethod
    def select(cls, sql, value: tuple) -> Cursor:
        return cls.execute_select(sql=sql, value=value)

    @classmethod
    def is_exists(cls, ip, table: str, port: int = None, protocol=None) -> bool:
        """
        :param table:  要查询的表  . 目前只有两个表格，一个 proxy_ip ,一个 verified_proxy
        :param ip:
        :param port:
        :param protocol:
        :return: True 代表存在，False代表不存在
        """

        if table == 'proxy_ip' or table == 'verified_proxy':  # 必须执行表格名称
            if port is not None and protocol is not None:
                sql = f"select * from `{table}` where ip = ? and port = ? and support_protocol = ?"
                value = (ip, port, protocol)
                res = cls.execute_select(sql=sql, value=value)
                if res is None:
                    pass
                else:
                    if res.fetchone():
                        return True
                    else:
                        return False

            elif protocol is None and port is not None:
                sql = f"select * from `{table}` where ip = ? and port = ?"
                value = (ip, port,)
                res = cls.execute_select(sql=sql, value=value)
                if res is None:
                    pass
                else:
                    if res.fetchone():
                        return True
                    else:
                        return False
            else:
                sql = f"select * from `{table}` where ip = ?"
                value = (ip,)
                res = cls.execute_select(sql=sql, value=value)
                if res is None:
                    pass
                else:
                    if res.fetchone():
                        return True
                    else:
                        return False
        else:
            logger.error(msg='you input table name is wrong. must declare which TABLE in sqlite3! ')
