from src.services.delivery.base_services import BaseService


class DeliveryService(BaseService):
    def __init__(self, delivery_repository, product_repository) -> None:
        super().__init__(delivery_repository)
        self.product_repository = product_repository

    def create_delivery(self, schema):
        return self.add(schema)

    def create_product_delivery(self, schema):
        products = schema.products
        delattr(schema, "products")
        delivery = self.add(schema)
        product_ids = []
        for product in products:
            product = product.dict()
            product["delivery_id"] = delivery.id
            prd_id = self.product_repository.add_product_delivery(product)
            product_ids.append(prd_id.dict())

        delivery = delivery.dict()
        delivery["products"] = product_ids
        return delivery
