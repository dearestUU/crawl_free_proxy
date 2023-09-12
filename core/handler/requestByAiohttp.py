# coding : utf-8
import asyncio
import platform
import time

import aiohttp
from aiohttp import ClientSession
from core import logger, coast_time
from core.handler.userAgent import get_1_random_ua
from core.setting import AIOHTTP_SEM, AIOHTTP_LIMIT, AIOHtTP_LIMIT_PER_PORT, AIOHTTP_URL_COUNT


async def download_link(target_url: str, session: ClientSession, **kwargs):
    """
    :param target_url: 目标url,只适合get请求,且请求页面是html
    :param session: clientSession
    :param kwargs: 用于更新 headers中内容
    :return:
    """

    # 设置http/http的请求头
    headers = {"User-Agent": get_1_random_ua()}
    headers.update(kwargs)

    # sem信标设置5，表示多少次http/https并发
    if AIOHTTP_SEM == 0:
        sem = 5
    else:
        sem = AIOHTTP_SEM

    async with asyncio.Semaphore(sem):
        # await asyncio.sleep(1)
        try:
            async with session.get(url=target_url, headers=headers, ssl=False) as resp:
                if resp.status == 200:
                    if resp.content_type == 'text/html' and resp.content_length is not None:
                        content = await resp.read()
                        if content is None:
                            return None, target_url
                        else:
                            return content, target_url
                    else:
                        return None, target_url
                else:
                    return None, target_url
        except asyncio.TimeoutError as err:
            msg = f"Timeout: {target_url} 原因:{err}"
            logger.error(msg=msg)
        except Exception as err1:
            msg = f"Exception: {target_url} 原因:{err1}"
            logger.error(msg=msg)


async def download_all(urlList: list, **kwargs):
    """
    :param urlList: 传入所有url的请求列表
    :param kwargs: 用于更新 headers中内容
    :return:
    """
    unfinished = []  # 响应未完成或响应不全的响应体
    finished = []  # 响应完成的http/https请求

    connector = aiohttp.TCPConnector(limit=AIOHTTP_LIMIT,
                                     limit_per_host=AIOHtTP_LIMIT_PER_PORT)  # limit默认100，limit=0的时候是无限制;limit_per_host,同一端口连接数量
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.ensure_future(download_link(target_url=url, session=session, **kwargs)) for url in urlList]

        for resp in await asyncio.gather(*tasks, return_exceptions=True):
            try:
                resp_data = resp[0]
                resp_url = resp[1]
                if resp_data is None:
                    unfinished.append(resp_url)
                else:
                    finished.append([resp_data, resp_url])
            except Exception as ex:
                logger.error(msg=f">>> 服务器端响应出现问题: {ex}")
                unfinished.append(resp_url)

    return finished, unfinished


def download_main(urlList: list, **kwargs):
    """
    :param urlList: 传入所有url的请求列表
    :param kwargs: 用于更新 headers中内容
    :return:
    """
    if "windows" in platform.platform().lower():
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # python3.8 以上的windows
        return asyncio.run(download_all(urlList=urlList, **kwargs))
    else:
        return asyncio.run(download_all(urlList=urlList, **kwargs))  # MAC/Linux 对aiohttp兼容性好


class T:
    download_main_count = 0

    @staticmethod
    def split_url_list(urlList: list):
        """
        :param urlList: 传入的url列表
        :return: 每次请求50个，并以list的形式返回
        """
        logger.info(msg=f'Total of request {len(urlList)} urls, please waiting for response...')

        count_of_url = len(urlList)  # 请求url的总条数
        count_of_aiohttp = int(count_of_url / AIOHTTP_URL_COUNT) + 1  # 要用aiohttp模块请求次数

        if count_of_url > 0:
            ___ = []  # 被分隔得urlList列表
            len_count_of_url = len(urlList)  # 请求url的总条数
            a = 0
            b = AIOHTTP_URL_COUNT
            tmp = 0
            for _ in range(0, count_of_aiohttp):
                if len_count_of_url > AIOHTTP_URL_COUNT:  # 如果传入得urlList大于50个
                    len_count_of_url -= AIOHTTP_URL_COUNT  # 每次自减50
                    ___.append(urlList[a:b])
                    # print(f">>> 要用aiohttp请求{count_of_aiohttp}次: 这是第 {tmp + 1}次请求,需请求{b - a}条数据.")
                    a += AIOHTTP_URL_COUNT
                    b += AIOHTTP_URL_COUNT
                else:
                    ___.append(urlList[a:])
                    # print(f">>> 要用aiohttp请求{count_of_aiohttp}次: 这是第 {tmp + 1}次请求,需请求{count_of_url - (tmp * AIOHTTP_URL_COUNT)}条数据.")
                tmp += 1
            return ___, count_of_url
        else:
            return None

    @staticmethod
    def request_by_aiohttp(splitList: list, **kwargs):
        """
        :param splitList: 传入所有url的请求列表
        :param kwargs: 用于更新 headers中内容
        :return: 接收 split_url_list 传过来得参数
        """
        finished = []
        unfinished = []

        for urlList in splitList:
            T.download_main_count += 1
            time1 = time.time()
            result = download_main(urlList=urlList, **kwargs)
            time2 = time.time()
            logger.info(f">>> {T.download_main_count} request coast {(time2 - time1):6f} seconds.")
            res1 = result[0]  # 完成响应后得html
            res2 = result[1]  # 未完成响应得url
            finished += res1
            unfinished += res2
        return finished, unfinished

    @staticmethod
    @coast_time
    def T_MAIN(urlList: list, **kwargs):
        """
        :param urlList: 传入所有url的请求列表
        :param kwargs: 用于更新 headers中内容
        :return: 返回所有url请求后的结果
        """
        finished_url = []  # 已完成得url后得结果
        unfinished_url = []  # 未完成url

        param = T.split_url_list(urlList=urlList)
        if param is None:
            return None
        else:
            splitList = param[0]  # urlList 被分隔后得结果
            countUrl = param[1]  # url总数
            result = T.request_by_aiohttp(splitList=splitList, **kwargs)
            finished_url += result[0]
            unfinished_url += result[1]

            count = 0  # 计数
            if len(finished_url) == countUrl:
                logger.info(msg=f">>> {countUrl} urls have finished request and response!")
                return finished_url
            else:
                logger.warning(
                    msg=f">>> 第{count + 1}次请求.共计 {countUrl}个url,已经请求到{len(finished_url)}个url,继续处理中...")
                while 1:
                    if len(unfinished_url) != 0:
                        count += 1
                        param11 = T.split_url_list(urlList=unfinished_url)
                        param22 = param11[0]  # 未完成得请求url，被分隔成50个一组
                        param33 = param11[1]  # 未完成得请求url的个数
                        param44 = T.request_by_aiohttp(splitList=param22, **kwargs)  # 未完成的url再次使用aiohttp请求

                        param55 = param44[0]  # 再次使用aiohttp请求后的结果
                        param66 = param44[1]  # 再次使用aiohttp,但仍未完成请求的url

                        unfinished_url.clear()  # 先清空未完成url的列表
                        finished_url += param55
                        unfinished_url += param66
                        logger.warning(f">>> 第{count + 1}次请求.共计 {countUrl}个url,已经请求到{countUrl - param33}个url,还剩 {param33}个url没有请求,还在继续哦...")
                    else:
                        break
        return finished_url
