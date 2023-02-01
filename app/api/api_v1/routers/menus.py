from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.cache.cache import r_cache
from app.dependencies import get_db
from app.schemas.menus import Menu, MenuCreate, MenuUpdate
from app.service import service_menu

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
    menus = service_menu.get_menus(db)
    return menus


@router.get(
    '/menus/{menu_id}',
    response_model=Menu,
    summary='Read the menu',
    response_description='The menu by given id',
    description='Read the menu by given id',
)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = service_menu.get_menu(menu_id, db)
    if menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(menu))
    return menu


@router.post(
    '/menus/',
    status_code=201,
    response_model=Menu,
    summary='Create a menu',
    response_description='The created menu',
)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    created_menu = service_menu.create_menu(db=db, menu=menu)
    return created_menu


@router.patch(
    '/menus/{menu_id}',
    response_model=Menu,
    summary='Update the menu',
    response_description='The updated menu',
)
def update_menu(menu: MenuUpdate, menu_id: int, db: Session = Depends(get_db)):
    updated_menu = service_menu.update_menu(db=db, menu=menu, menu_id=menu_id)
    if updated_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return updated_menu


@router.delete(
    '/menus/{menu_id}',
    summary='Delete the menu',
    description='Delete the menu with given id',
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    deleted = service_menu.delete_menu(db=db, menu_id=menu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='menu not found')
    return {'status': True, 'message': 'The menu has been deleted'}
