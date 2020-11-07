import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tests.utils import Base


@pytest.fixture(
    scope="session",
    params=[
        "sqlite:///",
        "postgresql://postgres:postgres@localhost:5432/test",
        "mysql://mysql:mysql@127.0.0.1:3306/test",
    ],
)
def engine(request):
    return create_engine(request.param)


@pytest.fixture(scope="session")
def connection(engine):
    _connection = engine.connect()
    yield _connection
    _connection.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database(connection):
    Base.metadata.create_all(bind=connection)


@pytest.fixture()
def session(connection):
    trans = connection.begin()

    _session = Session(bind=connection)
    yield _session
    _session.close()

    trans.rollback()
