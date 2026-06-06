import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import get_session
from src.auth.dependencies import get_current_user_id


# =========================
# 1. DB TEST (SQLite mémoire)
# =========================
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def override_get_session():
    with Session(engine) as session:
        yield session


# =========================
# 2. USER FIXE POUR TESTS
# =========================
def override_get_user_id():
    return 1


# =========================
# 3. FIXTURES
# =========================
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user_id] = override_get_user_id

    with TestClient(app) as c:
        yield c