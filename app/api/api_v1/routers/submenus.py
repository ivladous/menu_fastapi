from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.submenus import Submenu, SubmenuCreate, SubmenuUpdate
from app.service import service_submenu

router = APIRouter(
    prefix='/menus',
    tags=['submenus'],
)


@router.get(
    '/{menu_id}/submenus/',
    response_model=list[Submenu],
    summary='Read all the submenus',
    response_description='All submenus',
)
def read_submenus(menu_id: int, db: Session = Depends(get_db)):
    submenus = service_submenu.get_submenus(db=db, menu_id=menu_id)
    return submenus


@router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=Submenu,
    summary='Read the submenu',
    description='Read the submenu by given id'
)
def read_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = service_submenu.get_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@router.post(
    '/{menu_id}/submenus/',
    status_code=201,
    response_model=Submenu,
    summary='Create a submenu',
    response_description='The created submenu',
)
def create_submenu(menu_id: int, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    created_submenu = service_submenu.create_submenu(db=db, menu_id=menu_id, submenu=submenu)
    return created_submenu


@router.patch(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=Submenu,
    summary='Update the submenu',
    response_description='The updated submenu',
)
def update_submenu(
        menu_id: int,
        submenu_id: int,
        submenu: SubmenuUpdate,
        db: Session = Depends(get_db),
):
    updated_submenu = service_submenu.update_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
    if updated_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return updated_submenu


@router.delete(
    '/{menu_id}/submenus/{submenu_id}',
    summary='Delete the submenu',
    description='Delete the submenu with given id',
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    deleted = service_submenu.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='submenu not found')
    return {'status': True, 'message': 'The submenu has been deleted'}
