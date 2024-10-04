from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class Delivery(SQLModel, table=True):
    __tablename__ = "delivery"
    id: int = Field(primary_key=True)
    client_name: str = Field(nullable=False)
    purchase_order: str = Field(nullable=False)
    seller_name: str = Field(nullable=False)
    delivery_address: str = Field(nullable=False)
    cep_delivery: str = Field(nullable=False)
    days_for_delivery: int = Field(nullable=False)
    priority_name: str = Field(nullable=False)
    created_at: str = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    updated_at: str = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    deliverys: list["ProductDelivery"] = Relationship(back_populates="product_delivery", sa_relationship_kwargs={'lazy': 'joined'})
