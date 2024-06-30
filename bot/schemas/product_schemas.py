from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    brand_name: str
    supplier: str
    
class ProductOnPage(BaseModel):
    product: Product
    query: str
    page: int
    position: int