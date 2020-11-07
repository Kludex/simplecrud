import pytest
from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from crud_factory.factories import CRUDFactory

Base = declarative_base()


@pytest.fixture(params=["sqlite:///", "postgresql://postgres:postgres@localhost/test"])
def engine(request):
    return create_engine(request.param)


@pytest.fixture(autouse=True)
def setup_database(engine):
    Base.metadata.create_all(engine)


@pytest.fixture()
def session(engine):
    _session = Session(bind=engine)
    yield _session
    _session.close()


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


def test_create_with_dict(session: Session):
    crud_user = CRUDFactory.get_sqlalchemy(User, UserCreate, UserUpdate)
    obj = crud_user.create(session, {"name": "Potato", "age": 7})
    assert obj.age == 7 and obj.name == "Potato", UserOut.from_orm(obj)


def test_create_with_pydantic(session: Session):
    crud_user = CRUDFactory.get_sqlalchemy(User, UserCreate, UserUpdate)
    obj = crud_user.create(session, UserCreate(name="Potato", age=7))
    assert obj.age == 7 and obj.name == "Potato", UserOut.from_orm(obj)


def test_create_wrong_column_name(session: Session):
    crud_user = CRUDFactory.get_sqlalchemy(User, UserCreate, UserUpdate)
    with pytest.raises(TypeError):
        crud_user.create(session, {"name": "Potato", "wrong": 7})


# NOTE: This works on SQLite.
def test_create_wrong_value_type(session: Session):
    crud_user = CRUDFactory.get_sqlalchemy(User, UserCreate, UserUpdate)
    obj = crud_user.create(session, {"name": "Potato", "age": "Potato"})
    assert obj.age == "Potato" and obj.name == "Potato", UserOut.from_orm(obj)
