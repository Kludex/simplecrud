import pytest
from sqlalchemy.orm.session import Session

from tests.utils import User, UserOut, crud_user

VALID_DATA = {"name": "Potato", "age": 7}


@pytest.mark.parametrize(
    "args,kwargs",
    [
        ([], {"name": "Potato"}),
        ([], {"age": 7}),
        ([User.name == "Potato"], {}),
        ([User.age == 7], {}),
    ],
)
def test_delete(session: Session, args: list, kwargs: dict):
    obj_in = crud_user.create(session, VALID_DATA)
    obj_out = crud_user.delete(session, *args, **kwargs)
    assert UserOut.from_orm(obj_in) == UserOut.from_orm(obj_out)


@pytest.mark.parametrize(
    "args,kwargs",
    [
        ([], {"name": "otatoP"}),
        ([], {"age": 8}),
        ([User.name == "otatoP"], {}),
        ([User.age == 8], {}),
    ],
)
def test_delete_not_found(session: Session, args: list, kwargs: dict):
    crud_user.create(session, VALID_DATA)
    crud_user.delete(session, *args, **kwargs)


@pytest.mark.parametrize(
    "args,kwargs",
    [
        ([], {"name": "Potato"}),
        ([], {"age": 7}),
        ([User.name == "Potato"], {}),
        ([User.age == 7], {}),
    ],
)
def test_delete_multiple_rows(session: Session, args: list, kwargs: dict):
    crud_user.create(session, VALID_DATA)
    crud_user.create(session, VALID_DATA)
    crud_user.delete(session, *args, **kwargs)
    assert crud_user.count(session, **VALID_DATA) == 1
