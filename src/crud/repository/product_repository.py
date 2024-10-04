from sqlalchemy.orm import joinedload

from src.crud.models.products import Product, ProductDelivery
from src.crud.repository.base_repository import BaseRepository
from src.infra.commons.exceptions import NotFoundError
from src.infra.settings import settings
from src.utils.query_builder import dict_to_sqlalchemy_filter_options


class ProductRepository(BaseRepository):
    def __init__(self, session_factory) -> None:
        super().__init__(session_factory, Product)

    def create(self, schema):
        with self.session_factory() as session:
            if isinstance(schema, dict):
                query = self.model(**schema)
            else:
                query = self.model(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query
            except Exception as e:
                session.rollback()
                raise e

    def update(self, schema, id):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            try:
                for key, value in schema.dict().items():
                    setattr(query, key, value)
                session.commit()
                session.refresh(query)
                return query
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            try:
                session.delete(query)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def read_by_id(self, usr_id: int, eager=False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            query = query.filter(self.model.id == usr_id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {usr_id}")
            return query

    def add_product_delivery(self, schema):
        with self.session_factory() as session:
            if isinstance(schema, dict):
                query = ProductDelivery(**schema)
            else:
                query = ProductDelivery(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query
            except Exception as e:
                session.rollback()
                raise e

    def read_by_options(self, schema, eager=False):
        with self.session_factory() as session:
            schema_as_dict = schema.dict(exclude_none=True)
            page = schema_as_dict.get("page", settings.PAGE)
            page_size = schema_as_dict.get("page_size", settings.PAGE_SIZE)
            filter_options = dict_to_sqlalchemy_filter_options(self.model, schema.dict(exclude_none=True))
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            filtered_query = query.filter(filter_options)
            if page_size == "all":
                query = query.all()
            else:
                query = query.limit(page_size).offset((page - 1) * page_size).all()
            total_count = filtered_query.count()
            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                },
            }
