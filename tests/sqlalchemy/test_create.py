import pytest
from sqlalchemy.exc import DataError, OperationalError
from sqlalchemy.orm.session import Session

from tests.utils import UserCreate, UserOut, crud_user


def test_create_with_dict(session: Session):
    obj = crud_user.create(session, {"name": "Potato", "age": 7})
    assert obj.age == 7 and obj.name == "Potato", UserOut.from_orm(obj)


def test_create_with_pydantic(session: Session):
    obj = crud_user.create(session, UserCreate(name="Potato", age=7))
    assert obj.age == 7 and obj.name == "Potato", UserOut.from_orm(obj)


def test_create_wrong_column_name(session: Session):
    with pytest.raises(TypeError):
        crud_user.create(session, {"name": "Potato", "wrong": 7})


def test_create_wrong_value_type(session: Session):
    if session.bind.engine.url.drivername in ("sqlite"):
        pytest.skip()
    with pytest.raises((DataError, OperationalError)):
        crud_user.create(session, {"name": "Potato", "age": "Potato"})
