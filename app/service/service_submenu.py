from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.cache.cache import r_cache
from app.crud import crud_menu, crud_submenu
from app.schemas.submenus import SubmenuCreate, SubmenuUpdate


def get_submenus(db: Session, menu_id: int):
    db_submenus = crud_submenu.get_submenus(db, menu_id)
    return db_submenus


def get_submenu(menu_id: int, submenu_id: int, db: Session):
    if r_cache.exists(f'submenu:{submenu_id}'):
        cache_submenu = r_cache.json().get(f'submenu:{submenu_id}')
        return cache_submenu
    db_submenu = crud_submenu.get_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    return db_submenu


def create_submenu(db: Session, menu_id: int, submenu: SubmenuCreate):
    created_submenu = crud_submenu.create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    db_submenu = crud_submenu.get_submenu(db=db, menu_id=menu_id, submenu_id=created_submenu.id)
    if r_cache.exists(f'menu:{menu_id}'):
        db_menu_updated = crud_menu.get_menu(db, menu_id=menu_id)
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu_updated))
    return db_submenu


def update_submenu(db: Session, menu_id: int, submenu_id: int, submenu: SubmenuUpdate):
    crud_submenu.update_submenu(db=db, submenu=submenu, menu_id=menu_id, submenu_id=submenu_id)
    db_submenu_updated = crud_submenu.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if r_cache.exists(f'submenu:{submenu_id}'):
        r_cache.json().set(f'submenu:{submenu_id}', '$', jsonable_encoder(db_submenu_updated))
    return db_submenu_updated


def delete_submenu(menu_id: int, submenu_id: int, db: Session):
    deleted_submenu = crud_submenu.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if not deleted_submenu:
        return deleted_submenu
    if r_cache.exists(f'submenu:{submenu_id}'):
        r_cache.json().delete(f'submenu:{submenu_id}')
    if r_cache.exists(f'menu:{menu_id}'):
        db_menu_updated = crud_menu.get_menu(db, menu_id=menu_id)
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu_updated))
    return deleted_submenu
