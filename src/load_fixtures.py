import json
import os
import sys

from sqlmodel import Session, create_engine, select

module_path = os.path.abspath(os.getcwd()) 
print(module_path)
if module_path not in sys.path:       
    sys.path.append(module_path)

from src.crud.models.products import Product
from src.crud.models.user import Modules, Permissions, Role, Unit
from src.infra.settings import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def load_json_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def insert_data(session, model, data_list):
    for data in data_list:
        query = select(model).where(model.id == data['id'])
        if not session.exec(query).first():
            item = model(**data)
            session.add(item)
    session.commit()
    session.close()


def load_modules():
    with Session(engine) as session:
        data = load_json_data('src/fixtures/modules.json')
        insert_data(session, Modules, data)


def load_permissions():
    with Session(engine) as session:
        data = load_json_data('src/fixtures/permissions.json')
        insert_data(session, Permissions, data)


def load_roles():
    with Session(engine) as session:
        data = load_json_data('src/fixtures/roles.json')
        insert_data(session, Role, data)


def load_products():
    with Session(engine) as session:
        data = load_json_data('src/fixtures/products.json')
        insert_data(session, Product, data)


def load_units():
    with Session(engine) as session:
        data = load_json_data('src/fixtures/units.json')
        insert_data(session, Unit, data)


if __name__ == '__main__':
    load_roles()
    load_modules()
    load_permissions()
    load_products()
    load_units()
