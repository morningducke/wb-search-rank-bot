from pydantic import BaseModel

class Product(BaseModel):
    # TODO: annotate with pydantic
    id: int
    name: str
    brand_name: str
    supplier: str
    
class ProductOnPage(BaseModel):
    product: Product
    query: str
    page: int
    position: int