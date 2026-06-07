# import pytest
# from fastapi.testclient import TestClient
# from sqlmodel import SQLModel, create_engine, Session
# from sqlalchemy.pool import StaticPool

# from src.main import app
# from src.database import get_session
# from src.auth.dependencies import get_current_user_id

# from src.models import User
# from passlib.context import CryptContext

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# # =========================
# # 1. DB TEST (SQLite mémoire)
# # =========================
# TEST_DATABASE_URL = "sqlite://"

# engine = create_engine(
#     TEST_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )


# def override_get_session():
#     with Session(engine) as session:
#         yield session


# # =========================
# # 2. USER FIXE POUR TESTS
# # =========================
# def override_get_user_id():
#     return 1


# # =========================
# # 3. FIXTURES
# # =========================
# @pytest.fixture(scope="session", autouse=True)
# def setup_db():

#     SQLModel.metadata.create_all(engine)

#     with Session(engine) as session:

#         user = User(
#             email="test@test.com",
#             hashed_password=pwd_context.hash("test")
#         )

#         session.add(user)
#         session.commit()

#     yield

#     SQLModel.metadata.drop_all(engine)


# @pytest.fixture
# def client():
#     app.dependency_overrides[get_session] = override_get_session
#     app.dependency_overrides[get_current_user_id] = override_get_user_id

#     with TestClient(app) as c:
#         yield c

import pytest
from pydantic_ai.models.test import TestModel
from src.ai.agent import agent
from fastapi.testclient import TestClient

from sqlmodel import (
    SQLModel,
    Session,
    create_engine
)

from sqlalchemy.pool import StaticPool

from passlib.context import CryptContext

from src.main import app
from src.models import User
from src.database import get_session
from src.auth.dependencies import get_current_user_id


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
@pytest.fixture(autouse=True)
def test_model():
    original_model = agent.model

    agent.model = TestModel()

    yield

    agent.model = original_model

# ==========================
# Base SQLite mémoire
# ==========================

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)


def override_get_session():
    with Session(engine) as session:
        yield session


def override_get_user_id():
    return 1


# ==========================
# Mock PydanticAI
# ==========================

# class FakeResult:
#     def __init__(self, output):
#         self.output = output


# def fake_run_sync(prompt):
#     return FakeResult(
#         "Réponse IA simulée"
#     )


@pytest.fixture(scope="session", autouse=True)
def setup_db():

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        user = User(
            email="test@test.com",
            hashed_password=pwd_context.hash(
                "test"
            )
        )

        session.add(user)
        session.commit()

    yield

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
# def mock_llm(monkeypatch):

#     from src.ai.agent import agent

#     monkeypatch.setattr(
#         agent,
#         "run_sync",
#         fake_run_sync
#     )


@pytest.fixture
def client():

    app.dependency_overrides[
        get_session
    ] = override_get_session

    app.dependency_overrides[
        get_current_user_id
    ] = override_get_user_id

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

