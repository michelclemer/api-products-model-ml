from fastapi import HTTPException

from src.crud.repository.user_repository import UserProfileRepository
from src.infra.auth.security import get_password_hash
from src.services.user.base_services import BaseService
from src.utils.hash import get_rand_hash


class UserService(BaseService):
    def __init__(self, user_repository):
        super().__init__(user_repository)

    def get_all_roles(self):
        return self._repository.get_all_roles()

    def create_user(self, user_info):
        user_info['user_token'] = get_rand_hash()
        if not user_info.get('password'):
            user_info['password'] = "123456"

        user_info['password'] = get_password_hash(user_info['password'])
        user = self._repository.get_by_email(user_info['email'])
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        role = self._repository.get_by_role_id(user_info['role_id'])
        created_user = self.add(user_info)
        self.create_role_user(role.id, created_user.id)
        permission = self.insert_permissions(user_info['permissions'], created_user)
        delattr(created_user, "password")
        response_user = created_user.dict()
        response_user['permissions'] = permission
        response_user['role'] = role.dict()
        response_user['profile'] = {}
        return response_user

    def get_profile(self, user_id: int):
        return self._repository.get_user_profile(user_id).dict()

    def insert_permissions(self, roles: dict, user) -> dict:
        all_modules = list(roles.keys())
        all_permissions = list(roles.values())
        data_response = {}
        for index, mod in enumerate(all_modules):
            try:
                perm = all_permissions[index]
                module_obj = self._repository.get_module_by_name(mod)
                permissions = {key: value for key, value in perm.items() if value}
                perms = permissions.keys()
                data = []
                for perm in perms:
                    permission_obj = self._repository.get_permission_by_name(perm)
                    user_permission = self._repository.create_user_permission(
                        {"user_id": user.id, "permission_id": permission_obj.id, "module_id": module_obj.id}
                    )
                    data.append(user_permission)
                format_data = self._format_user_response_json(data)
                data_response[module_obj.module_name] = format_data
            except Exception:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Error while creating user permissions",
                        "module": mod,
                        "permission": perm,
                    }
                )

        return data_response

    def create_role_user(self, role_id: str, user_id: int) -> None:
        self._repository.create_user_role(
            {"role_id": role_id, "user_id": user_id}
        )

    def _format_user_response_json(self, permision_list: list):
        result = {}
        for perm in permision_list:
            result[perm.permission.permisson_name] = True
        return result

    def list_units(self):
        return self._repository.list_units()


class ProfileService(BaseService):
    def __init__(self, profile_repository):
        self.profile_repository: UserProfileRepository = profile_repository
        super().__init__(profile_repository)

    def create_profile(self, schema):
        return self._repository.create(schema)

    def get_current_user_profile(self, user_id: int) -> dict:
        return self.profile_repository.get_current_profile(user_id).dict()

    def update_profile(self, prf_id: int, schema):
        return self._repository.update(prf_id, schema)
