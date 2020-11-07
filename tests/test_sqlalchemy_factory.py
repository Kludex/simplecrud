import pytest
from sqlalchemy.exc import DataError, OperationalError
from sqlalchemy.orm.session import Session

from crud_factory.factories import CRUDFactory
from tests.utils import User, UserCreate, UserOut, UserUpdate


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


def test_create_wrong_value_type(session: Session):
    if session.bind.url.drivername in ("sqlite"):
        pytest.skip()
    crud_user = CRUDFactory.get_sqlalchemy(User, UserCreate, UserUpdate)
    with pytest.raises((DataError, OperationalError)):
        crud_user.create(session, {"name": "Potato", "age": "Potato"})
