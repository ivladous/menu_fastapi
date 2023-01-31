from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Menu title example',
                'description': 'Menu description example',
            }
        }


class MenuUpdate(MenuBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Updated menu title example',
                'description': 'Updated menu description example',
            }
        }


class MenuInDBBase(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class Menu(MenuInDBBase):
    class Config:
        schema_extra = {
            'example': {
                'id': 104,
                'title': 'Menu title example',
                'description': 'Menu description example',
                'submenus_count': 10,
                'dishes_count': 20,
            }
        }
