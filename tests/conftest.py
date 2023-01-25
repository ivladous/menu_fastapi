from typing import Generator

import pytest
from starlette.testclient import TestClient

from main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def get_test_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def truncate_tables(get_test_db: Session):
    with get_test_db as test_db:
        test_db.execute('''TRUNCATE TABLE menu CASCADE;''')
        test_db.execute('''TRUNCATE TABLE submenu CASCADE;''')
        test_db.execute('''TRUNCATE TABLE dish;''')
        test_db.commit()


@pytest.fixture
def create_menu(get_test_db: Session):
    def wrapped_create_menu(title: str, description: str):
        with get_test_db as test_db:
            test_db.execute(
                f'''INSERT INTO menu (title, description) VALUES ('{title}', '{description}')'''
            )
            test_db.commit()
    return wrapped_create_menu


@pytest.fixture
def get_first_menu_id(get_test_db: Session):
    def wrapped_get_first_menu():
        with get_test_db as test_db:
            return test_db.execute('''SELECT id FROM menu LIMIT 1''').scalar()
    return wrapped_get_first_menu


@pytest.fixture
def create_submenu(get_test_db: Session):
    def wrapped_create_submenu(title: str, description: str, menu_id: int):
        with get_test_db as test_db:
            test_db.execute(
                f'''INSERT INTO submenu (title, description, menu_id) VALUES ('{title}', '{description}', {menu_id})'''
            )
            test_db.commit()
    return wrapped_create_submenu


@pytest.fixture
def get_first_submenu_id(get_test_db: Session):
    def wrapped_get_first_submenu():
        with get_test_db as test_db:
            return test_db.execute('''SELECT id FROM submenu LIMIT 1''').scalar()
    return wrapped_get_first_submenu


@pytest.fixture
def create_dish(get_test_db: Session):
    def wrapped_create_dish(title: str, description: str, price: int, submenu_id: int):
        with get_test_db as test_db:
            test_db.execute(
                f'''INSERT INTO dish (title, description, price, submenu_id) VALUES (
                '{title}', '{description}', {price}, {submenu_id}
                )'''
            )
            test_db.commit()
    return wrapped_create_dish


@pytest.fixture
def get_first_dish_id(get_test_db: Session):
    def wrapped_get_first_dish():
        with get_test_db as test_db:
            return test_db.execute('''SELECT id FROM dish LIMIT 1''').scalar()
    return wrapped_get_first_dish


@pytest.fixture
def data_menu():
    return {'title': 'Menu test title', 'description': 'Menu test description'}


@pytest.fixture
def new_data_menu():
    return {'title': 'Menu test title NEW', 'description': 'Menu test description NEW'}


@pytest.fixture()
def data_submenu():
    return {'title': 'Submenu test title', 'description': 'Submenu test description', 'menu_id': 1}


@pytest.fixture()
def new_data_submenu():
    return {'title': 'Submenu test title NEW', 'description': 'Submenu test description NEW', 'menu_id': 1}


@pytest.fixture()
def data_dish():
    return {
        'title': 'Dish test title',
        'description': 'Dish test description',
        'submenu_id': 1,
        'price': '100500.0'
    }


@pytest.fixture()
def new_data_dish():
    return {
        'title': 'Dish test title NEW',
        'description': 'Dish test description NEW',
        'submenu_id': 1,
        'price': '150.0',
    }


test_client = TestClient(app)

prefix: str = '/api/v1'
