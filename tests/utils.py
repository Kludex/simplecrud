from pydantic.main import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    age = Column(Integer)


class UserCreate(BaseModel):
    name: str
    age: int


class UserUpdate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True
