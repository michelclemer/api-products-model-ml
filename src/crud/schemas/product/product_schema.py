from typing import Optional

from pydantic import BaseModel

from src.crud.schemas.base_schema import FindBase
from src.crud.schemas.product.base_product import ProductBase
from src.utils.schema import partial_model


class ProductCreate(ProductBase):
    pass


@partial_model
class ProductUpdate(ProductBase):
    pass

@partial_model
class SearchProduct(FindBase):
    name__eq: Optional[str]
    code__eq: Optional[str]
    line__eq: Optional[str]
    weight__eq: Optional[float]
    size__eq: Optional[float]


class SetKeyRedis(BaseModel):
    key: str
    value: str
