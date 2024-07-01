from typing import Annotated
from bot.config import WbApiConfig
from bot.service.wbsearch_client import WBSearchClient
from bot.schemas.product_schemas import ProductOnPage
from pydantic import Field, StringConstraints, validate_call

@validate_call(config=dict(arbitrary_types_allowed=True))
async def get_search_position(query: Annotated[str, StringConstraints(min_length=1, max_length=WbApiConfig.MAX_QUERY_LENGTH)], 
                              item_id: Annotated[int, Field(ge=0)], 
                              client: WBSearchClient) -> ProductOnPage | None:
    """Выполняет поисковой запрос, аргументы валидируются с помощью pydantic"""
       
    product_on_page = await client.search(query=query, item_id=item_id)
    return product_on_page
        