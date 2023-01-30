from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.models.models import DishModel, MenuModel, SubmenuModel
from app.schemas.menus import MenuCreate, MenuUpdate


def get_menus(db: Session):
    return (
        db.query(
            MenuModel.id,
            MenuModel.title,
            MenuModel.description,
            func.count(distinct(SubmenuModel.id)).label('submenus_count'),
            func.count(DishModel.id).label('dishes_count'),
        )
        .join(SubmenuModel, MenuModel.submenus, isouter=True)
        .join(DishModel, SubmenuModel.dishes, isouter=True)
        .group_by(MenuModel.id)
        .all()
    )


def get_menu(db: Session, menu_id: int):
    return (
        db.query(
            MenuModel.id,
            MenuModel.title,
            MenuModel.description,
            func.count(distinct(SubmenuModel.id)).label('submenus_count'),
            func.count(DishModel.id).label('dishes_count'),
        )
        .join(SubmenuModel, MenuModel.submenus, isouter=True)
        .join(DishModel, SubmenuModel.dishes, isouter=True)
        .filter(MenuModel.id == menu_id)
        .group_by(MenuModel.id)
        .first()
    )


def create_menu(db: Session, menu: MenuCreate):
    db_menu = MenuModel(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu: MenuUpdate, menu_id: int):
    updated_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).update(menu.dict())
    db.commit()
    return updated_menu


def delete_menu(db: Session, menu_id: int):
    deleted_menu = db.query(MenuModel).filter(MenuModel.id == menu_id).delete()
    db.commit()
    return deleted_menu
