from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud import crud_submenu
from app.schemas.menus import MenuUpdate
from app.schemas.submenus import Submenu, SubmenuCreate

router = APIRouter(
    prefix='/menus',
    tags=['submenus'],
)


@router.get('/{menu_id}/submenus/', response_model=list[Submenu])
def read_submenus(menu_id: int, db: Session = Depends(get_db)):
    db_submenus = crud_submenu.get_submenus(db=db, menu_id=menu_id)
    return db_submenus


@router.get("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
def read_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    db_submenu = crud_submenu.get_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@router.post('/{menu_id}/submenus/', status_code=201, response_model=Submenu)
def create_submenu(menu_id: int, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    created_submenu = crud_submenu.create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    db_submenu = crud_submenu.get_submenu(db=db, menu_id=menu_id, submenu_id=created_submenu.id)
    return db_submenu


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=Submenu)
def update_submenu(
        menu_id: int,
        submenu_id: int,
        submenu: MenuUpdate,
        db: Session = Depends(get_db),
):
    updated_submenu = crud_submenu.update_submenu(db=db, submenu=submenu, menu_id=menu_id, submenu_id=submenu_id)
    if not updated_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return crud_submenu.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)


@router.delete('/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    deleted_submenu = crud_submenu.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if not deleted_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return {"status": True, "message": "The submenu has been deleted"}
