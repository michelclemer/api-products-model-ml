class BaseService:
    def __init__(self, repository) -> None:
        self._repository = repository

    def get_list(self, schema):
        return self._repository.read_by_options(schema)

    def get_by_id(self, pk: int):
        return self._repository.read_by_id(pk)

    def add(self, schema):
        return self._repository.create(schema)

    def patch(self, pk: int, schema):
        return self._repository.update(pk, schema)

    def patch_attr(self, pk: int, attr: str, value):
        return self._repository.update_attr(pk, attr, value)

    def put_update(self, pk: int, schema):
        return self._repository.whole_update(pk, schema)

    def remove_by_id(self, pk: int):
        return self._repository.delete_by_id(pk)

    def create_role(self, schema):
        return self._repository.create_role(schema)

    def create_role_user(self, schema):
        return self._repository.create_role_user(schema)

    def get_by_email(self, email):
        return self._repository.read_by_email(email)
