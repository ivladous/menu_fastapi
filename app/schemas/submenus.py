from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Submenu title example',
                'description': 'Submenu description example',
            }
        }


class SubmenuUpdate(SubmenuBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Updated submenu title example',
                'description': 'Updated submenu description example',
            }
        }


class SubmenuInDBBase(SubmenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True


class Submenu(SubmenuInDBBase):
    class Config:
        schema_extra = {
            'example': {
                'id': 23,
                'title': 'Submenu title example',
                'description': 'Submenu description example',
                'dishes_count': 3,
            }
        }
