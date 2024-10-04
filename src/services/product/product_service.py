from src.services.product.base_services import BaseService


class ProductService(BaseService):
    def __init__(self, product_repository):
        super().__init__(product_repository)
