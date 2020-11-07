from pydantic.main import BaseModel


class UserBase(BaseModel):
    name: str
    age: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
