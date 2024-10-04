from dependency_injector import containers, providers

from src.crud.repository.delivery_repository import DeliveryRepository
from src.crud.repository.product_repository import ProductRepository
from src.crud.repository.user_repository import (UserProfileRepository,
                                                 UserRepository)
from src.infra.database import Database
from src.infra.redis import init_redis_pool
from src.infra.settings import settings
from src.services.delivery.delivery_service import DeliveryService
from src.services.product.product_service import ProductService
from src.services.redisService.redis_services import RedisService
from src.services.user.auth_service import AuthService
from src.services.user.user_services import ProfileService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src"])
    config = providers.Configuration()
    print(str(settings.SQLALCHEMY_DATABASE_URI))
    db = providers.Singleton(Database, db_url=str(settings.SQLALCHEMY_DATABASE_URI))

    redis_pool = providers.Resource(
        init_redis_pool,
        host=settings.REDIS_HOST,
        password=settings.REDIS_PASSWORD,
        port=settings.REDIS_PORT,
    )

    redis_service = providers.Factory(
        RedisService,
        redis=redis_pool,
    )

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    profile_repository = providers.Factory(UserProfileRepository, session_factory=db.provided.session)
    product_repository = providers.Factory(ProductRepository, session_factory=db.provided.session)
    delivery_repository = providers.Factory(DeliveryRepository, session_factory=db.provided.session)

    user_services = providers.Factory(UserService, user_repository=user_repository)
    auth_services = providers.Factory(AuthService, user_repository=user_repository)
    profile_services = providers.Factory(ProfileService, profile_repository=profile_repository)
    product_services = providers.Factory(ProductService, product_repository=product_repository)
    delivery_services = providers.Factory(DeliveryService, delivery_repository=delivery_repository, product_repository=product_repository)
