from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.dishes import Dish, DishCreate, DishUpdate
from app.service import service_dish

router = APIRouter(
    prefix='/menus',
    tags=['dishes'],
)


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/',
    response_model=list[Dish],
    summary='Read all the dishes',
    response_description='All dishes',
)
def read_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    dishes = service_dish.get_dishes(db=db, menu_id=menu_id, submenu_id=submenu_id)
    return dishes


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    summary='Read the dish',
    response_description='The dish by given id',
)
def read_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = service_dish.get_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes/',
    status_code=201,
    response_model=Dish,
    summary='Create a dish',
    response_description='The created dish',
)
def create_dish(menu_id: int, submenu_id: int, dish: DishCreate, db: Session = Depends(get_db)):
    created_dish = service_dish.create_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish=dish)
    return created_dish


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    summary='Update the dish',
    response_description='The updated dish',
)
def update_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish: DishUpdate,
        db: Session = Depends(get_db),
):
    updated_dish = service_dish.update_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dish=dish)
    if updated_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    return updated_dish


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    summary='Delete the dish',
    description='Delete the dish with given id',
)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    deleted = service_dish.delete_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='dish not found')
    return {'status': True, 'message': 'The dish has been deleted'}
