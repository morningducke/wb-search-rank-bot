from typing import Annotated
from bot.config import WbApiConfig
from bot.controller.wbsearch_client import WBSearchClient
from bot.schemas.product_schemas import ProductOnPage
from pydantic import Field, StringConstraints, validate_call

@validate_call
async def get_search_position(query: Annotated[str, StringConstraints(min_length=1, max_length=WbApiConfig.MAX_QUERY_LENGTH)], 
                              item_id: Annotated[int, Field(ge=0)], 
                              client: WBSearchClient) -> ProductOnPage:
    """Выполняет поисковой запрос, аргументы валидируются с помощью pydantic"""
       
    product_on_page = await client.search(query=query, item_id=item_id)
    return product_on_page
        
        
        
    
# @validate_call(config=dict(arbitrary_types_allowed=True))
# async def get_exchange_rate(base: CurrencyStr, query: CurrencyStr, client: ExchangeRateClient) -> ExchangeRate:
#     """Получает курс относительно базовой валюты

#     Args:
#         base (CurrencyStr): строка-идентификатор базовый валюты (пример: RUB)
#         query (CurrencyStr): строка-идентификатор валюты для сравнения с базовой
#         client (ExchangeRateClient): клиент, отправлюящий запросы к Exchange-Rate-API

#     Raises:
#         ValueError: возникает в случае ввода несуществующей валюты

#     Returns:
#         ExchangeRate: структура, содержащая строку базовой валюты, валюты для сравнения и курс (float)
#     """
    
#     rates = await client.request_rates(base)
#     if query not in rates:
#         raise ValueError
#     rate = rates[query]
#     return ExchangeRate(base_currency=base, query_currency=query, rate=rate)