import asyncio
from datetime import datetime, timezone
from random import random
from aiohttp import ClientSession

from bot.schemas.error_strings import Errors
from bot.schemas.product_schemas import Product, ProductOnPage
from bot.config import WbApiUrls, WbApiConfig

class WBSearchClient:
    """Клиент для общения с search.wb.ru"""

    def __init__(self, session: ClientSession, max_retries: int = 10, max_pages: int = 50, page_item_count: int = 100) -> None:
        """
        Args:
            session (ClientSession): aiohttp сессия
            max_retries (int, optional): максимальное количество повторов запросов в случае неудачи
            max_pages (int, optional): максимальное количество запрашиваемых страниц
            page_item_count (int, optional): количество товаров на странице
        """
        
        self._session = session
        self.max_retries = max_retries
        self.max_pages = max_pages
        self.page_item_count = page_item_count
        
    def _search_params_builder(self, query: str, page: int = None) -> dict:
        """Возвращает параметры для запроса"""
        
        params = dict(WbApiConfig.DEFAULT_SEARCH_PARAMS)
        params["query"] = query
        if page:
            query["page"] = page
        return params
    
    def _search_headers_builder(self, query_id : str = None) -> dict:
        """Возвращает заголовки для запроса"""
        
        headers = dict(WbApiConfig.DEFAULT_SEARCH_HEADERS)
        if query_id:
            headers["query_id"] = query_id
        return headers
        
    def _generate_query_id(self) -> str:
        """Генерирует header параметр x-queryid для поиска. Механизм взят отсюда https://github.com/glmn/wb-private-api/blob/main/src/Utils.js#L61.

        Returns:
            str: x-queryid
        """
        
        timestamp = int(datetime.now(timezone.utc).timestamp())  
        random_part = str(int(random() * 2**30))
        user_id = random_part + str(timestamp)
        return f"qid{user_id}{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")}"

    def _get_item_on_page(self, products: list[dict], id: int) -> tuple[int, dict] | None:        
        """Возвращает товар с позицией на странице, если он найден, иначе - None"""
        
        return next(((idx + 1, product) for idx, product in enumerate(products) if product["id"] == id), None)
    
        
    async def _get_search_page(self, query_params: dict, headers: dict = None) -> dict | None:
        """Получает страницу товаров при поиске с определенным запросом

        Args:
            query_params (dict): параметры поиска
            headers (dict, optional): заголовки запроса

        Returns:
            dict: страницу поиска: товары и общее кол-во товаров по данному запросу
        """
        
        request_string = WbApiUrls.search_endpoint 
        is_response_correct = False
        retries = 0
        data = None
        while not is_response_correct and retries <= self.max_retries:
            async with self._session.get(request_string, params=query_params, headers=headers) as response:
                    data = await response.json(content_type="text/plain")
                    is_response_correct = True if len(data["data"]["products"]) > 1 else False
                    if not is_response_correct:
                        await asyncio.sleep(0.2) # на всякий случай задержка между неудачными запросами
            retries += 1
                        
        if data and len(data["data"]["products"]) > 1:
            return data["data"]
                        
    async def search(self, query: str, item_id: int) -> ProductOnPage | None:
        """Возвращает положение (страница и позиция на странице) товара в поиске при определенном поисковом запросе.

        Args:
            query (str): поисковой запрос
            item_id (int): артикул товара

        Raises:
            ValueError: ошибка, указывающая на отсутствие товаров по запросу

        Returns:
            dict | None: словарь с положением товара и товаром. Если товар не найден, возвращается None.
        """
        
        query_id = self._generate_query_id()
        query_params = self._search_params_builder(query=query)
        headers = self._search_headers_builder(query_id=query_id)
        cur_page = 1 
        first_page = await self._get_search_page(query_params=query_params, headers=headers) 
        
        if not first_page:
            raise ValueError(Errors.GENERAL)
      
        # получение кол-ва товаров по данному запросу для формирования максимального кол-ва запрашиваемых страниц
        total_items = first_page["total"]
        if total_items == 0:
            raise ValueError(Errors.NO_PRODUCTS)
        
        item = self._get_item_on_page(products=first_page["products"], id=item_id)
        
        # если не на первой странице
        if not item:
            max_pages = min(self.max_pages, 1 + total_items // self.page_item_count)
            
            # запросы сразу на все страницы
            batched_params = [{**query_params, **{"page": i}} for i in range(2, max_pages + 1)]
            batched_pages = await asyncio.gather(*[self._get_search_page(query_params=p, headers=headers) for p in batched_params])
                
            for page_num, page in enumerate(batched_pages, start=2):
                item = self._get_item_on_page(products=page["products"], id=item_id)
                cur_page = page_num
                if item:
                    break
            
        if item:
            pos, product = item
            product = Product(id=product["id"], name=product["name"], brand_name=product["brand"], supplier=product["supplier"])
            return ProductOnPage(product=product, page=cur_page, position=pos, query=query)
        
        
    
        