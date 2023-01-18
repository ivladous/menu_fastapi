from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuBase):
    pass


class SubmenuInDBBase(SubmenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True


class Submenu(SubmenuInDBBase):
    pass
