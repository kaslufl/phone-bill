import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from phone_bill.app import app
from phone_bill.core.external.schema import table_registry
from phone_bill.infrastructure.database.database import get_session


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:

        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)
