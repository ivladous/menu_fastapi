from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str


class DishCreate(DishBase):
    price: float


class DishUpdate(DishCreate):
    pass


class DishInDBBase(DishBase):
    id: str
    price: str

    class Config:
        orm_mode = True


class Dish(DishInDBBase):
    pass
