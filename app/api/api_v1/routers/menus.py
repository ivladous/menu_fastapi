from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud import crud_menu
from app.dependencies import get_db
from app.schemas.menus import Menu, MenuCreate, MenuUpdate
from cache.cache import r_cache

router = APIRouter(
    tags=['menus'],
)


@router.get(
    '/menus/',
    response_model=list[Menu],
    summary='Read all the menus',
    response_description='All menus',
)
def read_menus(db: Session = Depends(get_db)):
    db_menus = crud_menu.get_menus(db)
    return db_menus


@router.get(
    '/menus/{menu_id}',
    response_model=Menu,
    summary='Read the menu',
    response_description='The menu by given id',
    description='Read the menu by given id',
)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    if r_cache.exists(f'menu:{menu_id}'):
        cache_menu = r_cache.json().get(f'menu:{menu_id}')
        return cache_menu
    db_menu = crud_menu.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu))
    return db_menu


@router.post(
    '/menus/',
    status_code=201,
    response_model=Menu,
    summary='Create a menu',
    response_description='The created menu',
)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    created_menu = crud_menu.create_menu(db=db, menu=menu)
    db_menu = crud_menu.get_menu(db, menu_id=created_menu.id)
    return db_menu


@router.patch(
    '/menus/{menu_id}',
    response_model=Menu,
    summary='Update the menu',
    response_description='The updated menu',
)
def update_menu(menu: MenuUpdate, menu_id: int, db: Session = Depends(get_db)):
    updated = crud_menu.update_menu(db=db, menu=menu, menu_id=menu_id)
    if not updated:
        raise HTTPException(status_code=404, detail='menu not found')
    db_menu_updated = crud_menu.get_menu(db, menu_id=menu_id)
    if r_cache.exists(f'menu:{menu_id}'):
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu_updated))
    return db_menu_updated


@router.delete(
    '/menus/{menu_id}',
    summary='Delete the menu',
    description='Delete the menu with given id',
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    deleted = crud_menu.delete_menu(db=db, menu_id=menu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='menu not found')
    if r_cache.exists(f'menu:{menu_id}'):
        r_cache.json().delete(f'menu:{menu_id}')
    return {'status': True, 'message': 'The menu has been deleted'}
