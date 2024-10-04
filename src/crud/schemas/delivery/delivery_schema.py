from typing import Optional

from src.crud.schemas.base_schema import FindBase
from src.crud.schemas.delivery.base_delivery import (DeliveryBase,
                                                     ProductDeliveryCreate)
from src.utils.schema import partial_model


class DeliveryCreate(DeliveryBase):
    products: list[ProductDeliveryCreate]


@partial_model
class DeliveryUpdate(DeliveryBase):
    pass


@partial_model
class SearchDelivery(FindBase):
    client_name__eq: Optional[str]
    purchase_order__eq: Optional[str]
    seller_name__eq: Optional[str]
    delivery_address__eq: Optional[str]
    cep_delivery__eq: Optional[str]
    days_for_delivery__eq: Optional[int]
    priority_name__eq: Optional[str]
    created_at__eq: Optional[str]
    updated_at__eq: Optional[str]
    created_at__lt: Optional[str]
    created_at__gt: Optional[str]
    updated_at__lt: Optional[str]
    updated_at__gt: Optional[str]
