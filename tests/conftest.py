# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.models import Base
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL, connect_args={
        "check_same_thread": False})
SessionLocalTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create all tables in the in-memory SQLite database at the start of the test session.
    Drop them when the session finishes.
    """
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    """
    Provide a SQLAlchemy session (connected to the test DB),
    and roll back after each test if needed.
    """
    session = SessionLocalTest()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session):
    """
    Create a TestClient using the test database session.
    Override the `init_db` dependency so all endpoint calls use `db_session`.
    """
    from app.db.database import init_db

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[init_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def user1_fixture(db_session):
    from app.db.crud.crud_user import create_user
    user1 = create_user(username="test_user1", api_key="a5LUP2wj3")
    return user1


@pytest.fixture
def user2_fixture(db_session):
    from app.db.crud.crud_user import create_user
    user2 = create_user(username="test_user2", api_key="a5LUP2wj332casd65")
    return user2
