from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str


class DishCreate(DishBase):
    price: float

    class Config:
        schema_extra = {
            'example': {
                'title': 'Dish title example',
                'description': 'Dish description example',
                'price': 610.9,
            }
        }


class DishUpdate(DishCreate):
    class Config:
        schema_extra = {
            'example': {
                'title': 'Updated dish title example',
                'description': 'Updated dish description example',
                'price': 450.3,
            }
        }


class DishInDBBase(DishBase):
    id: str
    price: str

    class Config:
        orm_mode = True


class Dish(DishInDBBase):
    class Config:
        schema_extra = {
            'example': {
                'id': 30,
                'title': 'Dish title example',
                'description': 'Dish description example',
                'price': 610.8,
            }
        }
