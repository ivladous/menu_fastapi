from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import DishModel, SubmenuModel
from app.schemas.menus import MenuUpdate
from app.schemas.submenus import SubmenuCreate


def get_submenus(db: Session, menu_id: int):
    return (
        db.query(
            SubmenuModel.id,
            SubmenuModel.title,
            SubmenuModel.description,
            func.count(DishModel.id).label('dishes_count'),
        )
        .join(DishModel, SubmenuModel.dishes, isouter=True)
        .filter(SubmenuModel.menu_id == menu_id)
        .group_by(SubmenuModel.id)
        .all()
    )


def get_submenu(db: Session, menu_id: int, submenu_id: int):
    return (
        db.query(
            SubmenuModel.id,
            SubmenuModel.title,
            SubmenuModel.description,
            func.count(DishModel.id).label('dishes_count'),
        )
        .join(DishModel, SubmenuModel.dishes, isouter=True)
        .filter(SubmenuModel.menu_id == menu_id, SubmenuModel.id == submenu_id)
        .group_by(SubmenuModel.id)
        .first()
    )


def create_submenu(db: Session, submenu: SubmenuCreate, menu_id: int):
    db_submenu = SubmenuModel(**submenu.dict(), menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session, submenu: MenuUpdate, menu_id: int, submenu_id: id):
    updated_submenu = (
        db.query(SubmenuModel)
        .filter(SubmenuModel.menu_id == menu_id, SubmenuModel.id == submenu_id)
        .update(submenu.dict())
    )
    db.commit()
    return updated_submenu


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    deleted_submenu = (
        db.query(SubmenuModel)
        .filter(SubmenuModel.menu_id == menu_id, SubmenuModel.id == submenu_id)
        .delete()
    )
    db.commit()
    return deleted_submenu
