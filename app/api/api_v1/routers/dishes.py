from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud import crud_dish
from app.schemas.dishes import Dish, DishCreate, DishUpdate

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
    db_dish = crud_dish.get_dish(db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@router.post('/{menu_id}/submenus/{submenu_id}/dishes/', status_code=201, response_model=Dish)
def create_dish(submenu_id: int, dish: DishCreate, db: Session = Depends(get_db)):
    created_dish = crud_dish.create_dish(db=db, submenu_id=submenu_id, dish=dish)
    return created_dish


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=Dish)
def update_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int, dish:
        DishUpdate,
        db: Session = Depends(get_db)
):
    print(crud_dish.exists_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id))
    if not crud_dish.exists_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id):
        raise HTTPException(status_code=404, detail="dish not found")
    updated_dish = crud_dish.update_dish(db=db, dish=dish, dish_id=dish_id)
    print(updated_dish)
    return crud_dish.get_dish(db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    if not crud_dish.exists_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id):
        raise HTTPException(status_code=404, detail="dish not found")
    deleted_dish = crud_dish.delete_dish(db=db, dish_id=dish_id)
    return {"deleted": deleted_dish, "status": True, "message": "The dish has been deleted"}
