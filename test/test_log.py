# coding : utf-8

from core import logger,logger_r

def test1():
    logger.info(msg="test info")
    logger.error(msg='test error')
    logger.warning(msg='test warning')


if __name__ == '__main__':
    test1()
