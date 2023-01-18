from sqlalchemy.orm import Session

from app.models.models import DishModel, MenuModel, SubmenuModel
from app.schemas.dishes import DishCreate, DishUpdate


def get_dishes(db: Session, menu_id: int, submenu_id: int):
    return (
        db.query(DishModel)
        .select_from(MenuModel)
        .join(SubmenuModel, MenuModel.submenus)
        .join(DishModel, SubmenuModel.dishes)
        .filter(
            MenuModel.id == menu_id,
            SubmenuModel.id == submenu_id,
        )
        .all()
    )


def get_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    return (
        db.query(DishModel)
        .select_from(MenuModel)
        .join(SubmenuModel, MenuModel.submenus)
        .join(DishModel, SubmenuModel.dishes)
        .filter(
            MenuModel.id == menu_id,
            SubmenuModel.id == submenu_id,
            DishModel.id == dish_id,
        )
        .first()
    )


def create_dish(db: Session, dish: DishCreate, submenu_id: int):
    db_dish = DishModel(**dish.dict(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def exists_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    return (
        db.query(
            db.query(DishModel)
            .select_from(MenuModel)
            .join(SubmenuModel, MenuModel.submenus)
            .join(DishModel, SubmenuModel.dishes)
            .filter(
                MenuModel.id == menu_id,
                SubmenuModel.id == submenu_id,
                DishModel.id == dish_id,
            )
            .exists()
        )
        .scalar()
    )


def update_dish(db: Session, dish: DishUpdate, dish_id: int):
    updated_dish = (
        db.query(DishModel)
        .filter(DishModel.id == dish_id)
        .update(dish.dict())
    )
    db.commit()
    return updated_dish


def delete_dish(db: Session, dish_id: int):
    deleted_dish = (
        db.query(DishModel)
        .filter(DishModel.id == dish_id)
        .delete()
    )
    db.commit()
    return deleted_dish
