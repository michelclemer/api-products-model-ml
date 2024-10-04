from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.crud.schemas.delivery.delivery_schema import (DeliveryCreate,
                                                       SearchDelivery)
from src.infra.auth.security import JWTBearer
from src.infra.container import Container
from src.services.delivery.delivery_service import DeliveryService

router = APIRouter()


@router.get("/delivery/", dependencies=[Depends(JWTBearer())])
@inject
def get_delivery(
        find_query: SearchDelivery = Depends(),
        delivery_service: DeliveryService = Depends(Provide[Container.delivery_services])
):
    return delivery_service.get_list(find_query)


@router.post("/delivery/")
@inject
def post_delivery(
        schema: DeliveryCreate,
        delivery_service: DeliveryService = Depends(Provide[Container.delivery_services])
):
    return delivery_service.create_product_delivery(schema)
