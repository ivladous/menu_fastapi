from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud import crud_dish, crud_menu, crud_submenu
from app.schemas.dishes import Dish, DishCreate, DishUpdate
from cache.cache import r_cache

router = APIRouter(
    prefix='/menus',
    tags=['dishes'],
)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/', response_model=list[Dish])
def read_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    db_dishes = crud_dish.get_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id)
    return db_dishes


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
def read_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    if r_cache.exists(f'dish:{dish_id}'):
        cache_dish = r_cache.json().get(f'dish:{dish_id}')
        return cache_dish
    db_dish = crud_dish.get_dish(db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@router.post('/{menu_id}/submenus/{submenu_id}/dishes/', status_code=201, response_model=Dish)
def create_dish(menu_id: int, submenu_id: int, dish: DishCreate, db: Session = Depends(get_db)):
    created_dish = crud_dish.create_dish(db=db, submenu_id=submenu_id, dish=dish)
    if r_cache.exists(f'menu:{menu_id}'):
        db_menu_updated = crud_menu.get_menu(db, menu_id=menu_id)
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu_updated))
    if r_cache.exists(f'submenu:{submenu_id}'):
        db_submenu_updated = crud_submenu.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
        r_cache.json().set(f'submenu:{submenu_id}', '$', jsonable_encoder(db_submenu_updated))
    return created_dish


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=Dish)
def update_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int, dish:
        DishUpdate,
        db: Session = Depends(get_db)
):
    if not crud_dish.exists_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id):
        raise HTTPException(status_code=404, detail="dish not found")
    updated_dish = crud_dish.update_dish(db=db, dish=dish, dish_id=dish_id)
    db_dish_updated = crud_dish.get_dish(db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if r_cache.exists(f'dish:{dish_id}'):
        r_cache.json().set(f'dish:{dish_id}', '$', jsonable_encoder(db_dish_updated))
    return db_dish_updated


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    if not crud_dish.exists_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id):
        raise HTTPException(status_code=404, detail="dish not found")
    deleted_dish = crud_dish.delete_dish(db=db, dish_id=dish_id)
    if r_cache.exists(f'dish:{dish_id}'):
        r_cache.json().delete(f'dish:{dish_id}')
    if r_cache.exists(f'menu:{menu_id}'):
        db_menu_updated = crud_menu.get_menu(db, menu_id=menu_id)
        r_cache.json().set(f'menu:{menu_id}', '$', jsonable_encoder(db_menu_updated))
    if r_cache.exists(f'submenu:{submenu_id}'):
        db_submenu_updated = crud_submenu.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
        r_cache.json().set(f'submenu:{submenu_id}', '$', jsonable_encoder(db_submenu_updated))
    return {"deleted": deleted_dish, "status": True, "message": "The dish has been deleted"}
