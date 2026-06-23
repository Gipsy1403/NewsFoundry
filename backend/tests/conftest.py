from pathlib import Path
import sys
import os
import pytest

# Ensure backend (project) is on sys.path so `src` is importable when pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

os.environ.setdefault("MISTRAL_API_KEY", "test-key")
# Définir ici les variables utilisées au moment de l'import des modules
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ.setdefault("WORLD_NEWS_API_KEY", "test-key")

from pydantic_ai.models.test import TestModel
from src.ai.agent import agent
from fastapi.testclient import TestClient

from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from passlib.context import CryptContext

from src.main import app
from src.models import User
from src.database import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(autouse=True)
def default_env(monkeypatch):
    """
    Fixture globale : s'assure de variables d'environnement cohérentes
    pour les tests (clé JWT, algorithme, durée token). Permet aussi
    d'isoler les appels réseaux par défaut (WORLD_NEWS_API_KEY absent).
    """
    # S'assurer d'une valeur par défaut pour la clé (certains tests vérifient l'absence)
    monkeypatch.setenv("WORLD_NEWS_API_KEY", "test-key")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    # Empêcher les appels réseau depuis `src.ai.news` en mockant requests.get
    try:
        import src.ai.news as ai_news

        class FakeResp:
            def raise_for_status(self):
                return None

            def json(self):
                return {"top_news": []}

        monkeypatch.setattr(ai_news.requests, "get", lambda *args, **kwargs: FakeResp())
    except Exception:
        pass

    yield


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
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def override_get_session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def session():
    with Session(engine) as s:
        yield s


def override_get_user_id():
    return 1


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(email="test@test.com", hashed_password=pwd_context.hash("test"))
        session.add(user)
        session.commit()

    yield

    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = override_get_session
    # Importer la dépendance ici afin qu'elle prenne en compte les env vars
    from src.auth.dependencies import get_current_user_id
    app.dependency_overrides[get_current_user_id] = override_get_user_id

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
