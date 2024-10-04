from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.crud.schemas.product.product_schema import SearchProduct, SetKeyRedis
from src.infra.container import Container
from src.services.product.product_service import ProductService
from src.services.redisService.redis_services import RedisService

router = APIRouter()

@router.get("/products/")
@inject
def get_products(
        find_query: SearchProduct = Depends(),
        product_service: ProductService = Depends(Provide[Container.product_services])
):
    """
    Sem o uso do container de injeção de dependência
    database = Database(db_url=str(settings.SQLALCHEMY_DATABASE_URI))
    session = database.session()

    # Instanciando o repositório e o serviço diretamente
    product_repository = ProductRepository(session_factory=session)
    product_service = ProductService(product_repository)

    return product_service.get_list(find_query)
    """
    return product_service.get_list(find_query)


@router.post("/create-redis/")
@inject
async def create_redis_key(item: SetKeyRedis = Depends(),  service: RedisService = Depends(Provide[Container.redis_service])):
    value = await service.set_key_value(item.key, item.value)
    return {"result": value}


@router.get("/get-redis/")
@inject
async def get_redis_key(service: RedisService = Depends(Provide[Container.redis_service])):
    value = await service.get_by_key()
    return {"result": value}
