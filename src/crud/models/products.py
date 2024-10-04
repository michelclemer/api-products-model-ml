from typing import List

from sqlmodel import Field, Relationship, SQLModel

from src.crud.models.delivery import Delivery


class Product(SQLModel, table=True):
    __tablename__ = "product"
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    code: str = Field(nullable=False)
    line: str = Field(nullable=False)
    weight: float = Field(nullable=True)
    size: float = Field(nullable=False)

    products: List["ProductDelivery"] | None = Relationship(back_populates="product_set", sa_relationship_kwargs={'lazy': 'joined'})


class ProductDelivery(SQLModel, table=True):
    __tablename__ = "product_delivery"
    id: int = Field(primary_key=True)
    delivery_id: int = Field(foreign_key="delivery.id")
    product_id: int = Field(foreign_key="product.id")
    is_bent: bool = Field(nullable=False)
    quantity: int = Field(nullable=True)
    product_set: Product | None = Relationship(back_populates="products", sa_relationship_kwargs={'lazy': 'joined'})
    product_delivery: "Delivery" = Relationship(back_populates="deliverys", sa_relationship_kwargs={'lazy': 'joined'})
