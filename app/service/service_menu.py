from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.cache.cache import r_cache
from app.crud import crud_menu
from app.schemas.menus import MenuUpdate


def get_menus(db: Session):
    db_menus = crud_menu.get_menus(db)
    return db_menus


def get_menu(menu_id: int, db: Session):
    if r_cache.exists(f'menu:{menu_id}'):
        cache_menu = r_cache.json().get(f'menu:{menu_id}')
        return cache_menu
    db_menu = crud_menu.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        return db_menu
    else:
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu))
        return db_menu


def create_menu(db: Session, menu: MenuUpdate):
    created_menu = crud_menu.create_menu(db=db, menu=menu)
    db_menu = crud_menu.get_menu(db, menu_id=created_menu.id)
    return db_menu


def update_menu(db: Session, menu: MenuUpdate, menu_id: int):
    crud_menu.update_menu(db=db, menu=menu, menu_id=menu_id)
    db_menu_updated = crud_menu.get_menu(db, menu_id=menu_id)
    if r_cache.exists(f'menu:{menu_id}'):
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu_updated))
    return db_menu_updated


def delete_menu(db: Session, menu_id: int):
    deleted = crud_menu.delete_menu(db=db, menu_id=menu_id)
    if r_cache.exists(f'menu:{menu_id}'):
        r_cache.json().delete(f'menu:{menu_id}')
    return deleted
