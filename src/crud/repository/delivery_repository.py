from sqlalchemy.orm import joinedload

from src.crud.models.delivery import Delivery
from src.crud.repository.base_repository import BaseRepository
from src.infra.commons.exceptions import NotFoundError
from src.infra.settings import settings
from src.utils.query_builder import dict_to_sqlalchemy_filter_options


class DeliveryRepository(BaseRepository):
    def __init__(self, session_factory) -> None:
        super().__init__(session_factory, Delivery)

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
            query_dict = [query.dict() for query in query]
            for index, q in enumerate(query):
                products = self.get_list_product(q.deliverys)
                query_dict[index]['products'] = products
            total_count = filtered_query.count()
            return {
                "founds": query_dict,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                },
            }

    def get_list_product(self, prod_list: list) -> list:
        res = []
        for prod in prod_list:
            payload = prod.product_set.dict()
            payload['quantity'] = prod.quantity
            payload['is_bent'] = prod.is_bent
            res.append(payload)
        return res
