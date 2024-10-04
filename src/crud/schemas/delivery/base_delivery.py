from typing import Optional

from pydantic import BaseModel


class ProductDeliveryCreate(BaseModel):
    product_id: int
    quantity: int
    is_bent: bool


class DeliveryBase(BaseModel):
    client_name: str
    purchase_order: str
    seller_name: str
    delivery_address: str
    cep_delivery: str
    days_for_delivery: int
    priority_name: str
