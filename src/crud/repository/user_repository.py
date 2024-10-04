from sqlalchemy.orm import joinedload

from src.crud.models.user import (Modules, Permissions, Role, Unit, User,
                                  UserLoginHistory, UserPermission,
                                  UserProfile, UserRole)
from src.crud.repository.base_repository import BaseRepository
from src.infra.commons.exceptions import NotFoundError
from src.infra.settings import settings
from src.utils.query_builder import dict_to_sqlalchemy_filter_options


class UserRepository(BaseRepository):
    def __init__(self, session_factory) -> None:
        super().__init__(session_factory, User)

    def get_all_roles(self):
        with self.session_factory() as session:
            query = session.query(Role).all()
            if not query:
                raise NotFoundError(detail="not found roles")
            return query

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

    def create_role(self, schema):
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

    def create_user_permission(self, schema):
        with self.session_factory() as session:
            if isinstance(schema, dict):
                query = UserPermission(**schema)
            else:
                query = UserPermission(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query
            except Exception as e:
                session.rollback()
                raise e

    def create_user_role(self, schema):
        with self.session_factory() as session:
            if isinstance(schema, dict):
                query = UserRole(**schema)
            else:
                query = UserRole(**schema.dict())
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

    def get_user_profile(self, user_id):
        with self.session_factory() as session:
            query = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if not query:
                raise NotFoundError(detail=f"not found user profile")
            return query

    def get_user_login_history(self, user_id):
        with self.session_factory() as session:
            query = session.query(UserLoginHistory).filter(UserLoginHistory.user_id == user_id).all()
            if not query:
                raise NotFoundError(detail=f"not found user login history")
            return query

    def read_by_id(self, usr_id: int, eager=False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            query = query.filter(self.model.id == usr_id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {usr_id}")
            user_permissions = query.user_permissions
            roles = [role.role_set.dict() for role in query.user_roles]
            profile = query.user_profile.dict() if query.user_profile else {}
            query = query.dict()
            all_modules = session.query(Modules).all()
            query["permissions"] = self._format_permissions(user_permissions, all_modules)
            query['role'] = roles[0] if roles else {}
            query['profile'] = profile
            del query["password"]
            return query

    def get_by_role_id(self, role_id):
        with self.session_factory() as session:
            query = session.query(Role).filter(Role.id == role_id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {role_id}")
            return query

    def _format_roles(self, roles):
        return [role.dict() for role in roles]

    def _format_permissions(self, permissions, modules):
        roles = {}
        for mod in modules:
            data = {}
            find_permissions = [role for role in permissions if role.module_id == mod.id]
            if any(find_permissions):
                for user_permission in find_permissions:
                    data[user_permission.permission.permisson_name] = True
            roles[mod.module_name] = data
        return roles

    def get_module_by_name(self, name):
        with self.session_factory() as session:
            query = session.query(Modules).filter(Modules.module_name == name).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            return query

    def get_permission_by_name(self, name):
        with self.session_factory() as session:
            query = session.query(Permissions).filter(Permissions.permisson_name == name).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            return query

    def read_by_options(self, schema, eager=False):
        with self.session_factory() as session:
            schema_as_dict = schema.dict(exclude_none=True)
            page = schema_as_dict.get("page", settings.PAGE)
            page_size = int(schema_as_dict.get("page_size", settings.PAGE_SIZE))
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

    def list_units(self):
        with self.session_factory() as session:
            query = session.query(Unit).all()
            if not query:
                raise NotFoundError(detail="not found units")
            return query


class UserProfileRepository(BaseRepository):
    def __init__(self, session_factory) -> None:
        super().__init__(session_factory, UserProfile)

    def create(self, schema):
        with self.session_factory() as session:
            query = self.model(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query
            except Exception as e:
                session.rollback()
                raise e

    def update(self, prf_id, schema):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.prf_id == prf_id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {prf_id}")
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
            query = session.query(self.model).filter(self.model.prf_id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            try:
                session.delete(query)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def get_current_profile(self, user_id):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == user_id).first()
            if not query:
                raise NotFoundError(detail=f"not found user profile")
            return query
