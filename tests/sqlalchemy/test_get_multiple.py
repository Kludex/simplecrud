from typing import List

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
        ([], {"name": "Apple"}, [{"name": "Apple", "age": 3}]),
        (
            [],
            {"name": "Potato"},
            [{"name": "Potato", "age": 7}, {"name": "Potato", "age": 6}],
        ),
        (
            [User.age >= 2],
            {},
            [
                {"name": "Potato", "age": 7},
                {"name": "Potato", "age": 6},
                {"name": "Apple", "age": 3},
                {"name": "Panana", "age": 2},
            ],
        ),
        (
            [User.name.like("%anana")],
            {},
            [
                {"name": "Banana", "age": 1},
                {"name": "Panana", "age": 2},
            ],
        ),
        ([], {}, VALID_DATA),
        ([User.age < 0], {}, []),
    ],
)
def test_get_multiple(session: Session, args: list, kwargs: dict, expect: List[dict]):
    for data in VALID_DATA:
        crud_user.create(session, data)
    objs = crud_user.get_multi(session, *args, **kwargs)

    assert [{"name": obj.name, "age": obj.age} for obj in objs] == expect


# TODO: Add tests with `offset`, `limit`, `order_by`
