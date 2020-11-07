import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tests.utils import Base


@pytest.fixture(
    params=[
        "sqlite:///",
        "postgresql://postgres:postgres@localhost:5432/test",
        "mysql://mysql:mysql@127.0.0.1:3306/test",
    ]
)
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
