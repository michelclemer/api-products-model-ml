from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    id: Optional[int]
    name: str
    code: str
    line: str
    weight: Optional[float]
    size: float
