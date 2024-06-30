from bot.schemas.product_schemas import Product, ProductOnPage


def build_product_string(product: Product) -> str:
    """Возвращает форматированную строку с информацией о продукте"""
    return (f"Артикул: {product.id}\n"
           f"Название: {product.name}\n"
           f"Брэнд: {product.brand_name}\n"
           f"Поставщик: {product.supplier}"
           ) 
           
def build_product_on_page_string(product_on_page: ProductOnPage) -> str:
    product_string = build_product_string(product=product_on_page.product)
    return (product_string + "\n"
           f"Поисковой запрос: {product_on_page.query}\n"
           f"Положение: страница {product_on_page.page}, позиция {product_on_page.position}\n"
           f"Абсолютная позиция: {(product_on_page.page - 1) * 100 + product_on_page.position}"
           )
           
    