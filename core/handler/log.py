# coding : utf-8
from datetime import datetime
import os
import sys
import logging
import colorlog


LOGGER = logging.getLogger("proxy")  # 日志记录器被创建
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)  # 使用指定的文件名创建一个FileHandler日志处理器，建议使用绝对路径

PRIMARY_FMT = "%(cyan)s[%(asctime)s] %(log_color)s[%(levelname)s]%(reset)s %(message)s"
CUSTOM_FMT = "%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s"

FORMATTER = colorlog.LevelFormatter(
    fmt={
        "DEBUG": PRIMARY_FMT,
        "INFO": PRIMARY_FMT,
        "WARNING": PRIMARY_FMT,
        "ERROR": PRIMARY_FMT,
        "CRITICAL": PRIMARY_FMT,
        "*": CUSTOM_FMT,
        "+": CUSTOM_FMT,
        "-": CUSTOM_FMT,
        "!": CUSTOM_FMT
    },
    datefmt="%H:%M:%S",
    log_colors={
        '*': 'cyan',
        '+': 'green',
        '-': 'red',
        '!': 'yellow',
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bg_red,white'
    },
    secondary_log_colors={},
    style='%'
)
LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(LOGGER_HANDLER)


def LOGGER_R():
    """
    :return: 记录日志到文件
    """
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    filename = 'logs' + datetime.now().strftime('%Y%m%d') + '.log'
    filepath = os.path.join(log_path, filename)
    if filename not in os.listdir(log_path):
        with open(filepath, 'a') as f:
            f.write('Start records log!\n')
    formatter = '[%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, filename=filepath, format=formatter, filemode='a+')
    return logging
