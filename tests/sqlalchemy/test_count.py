import pytest
from sqlalchemy.orm.session import Session

from tests.utils import User, crud_user

VALID_DATA = [
    {"name": "Potato", "age": 7},
    {"name": "Potato", "age": 6},
    {"name": "Apple", "age": 3},
    {"name": "Banana", "age": 1},
    {"name": "Panana", "age": 2},
]


@pytest.mark.parametrize(
    "args,kwargs,expect",
    [
        ([], {"name": "Apple"}, 1),
        ([], {"name": "Potato"}, 2),
        ([User.age >= 2], {}, 4),
        ([User.name.like("%anana")], {}, 2),
        ([], {}, 5),
        ([User.age < 0], {}, 0),
    ],
)
def test_get_multiple(session: Session, args: list, kwargs: dict, expect: int):
    for data in VALID_DATA:
        crud_user.create(session, data)
    count = crud_user.count(session, *args, **kwargs)

    assert count == expect
