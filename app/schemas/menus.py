from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuInDBBase(MenuBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class Menu(MenuInDBBase):
    pass
