from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    age: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password_hash: str
