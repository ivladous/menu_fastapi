from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class DishModel(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'))


class MenuModel(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship('SubmenuModel', backref='menu', cascade='all, delete')


class SubmenuModel(Base):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'))
    dishes = relationship('DishModel', backref='submenu', cascade='all, delete')
