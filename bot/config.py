from enum import StrEnum
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

class WbApiUrls(StrEnum):
    base_search_url = "https://search.wb.ru/exactmatch/ru/common/v5/"
    search_endpoint = "https://search.wb.ru/exactmatch/ru/common/v5/search"

class WbApiConfig:
    # базовые параметры, которые используются поисковом запросе на wildberries
    DEFAULT_SEARCH_PARAMS = {
        "ab_testing": "false",
        "appType" :	1,
        "curr": "rub",
        "dest" : -1257786, # москва
        "resultset" : "catalog",
        "sort" : "popular",
        "spp" : 30,
        "suppressSpellcheck" : "false"
    }
    DEFAULT_SEARCH_HEADERS = {
        "Host": "search.wb.ru",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": "https://www.wildberries.ru",
        "Connection": "keep-alive",
        "Referer": "https://www.wildberries.ru/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "Priority": "u=4"
    }
    MAX_QUERY_LENGTH = 300
