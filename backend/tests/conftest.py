from pathlib import Path
import os
import sys
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

# Ajoute le dossier backend au chemin Python.
# Cela permet à pytest d'importer correctement le package src.
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

# Définit des variables d'environnement factices pour les tests.
# Elles évitent les erreurs au moment de l'import de l'application.
os.environ.setdefault("MISTRAL_API_KEY", "test-key")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
os.environ.setdefault("WORLD_NEWS_API_KEY", "test-key")

from src.auth.dependencies import get_current_user_id
from src.database import get_session
from src.main import app
from src.models import User

# Contexte utilisé pour hasher le mot de passe du faux utilisateur de test.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crée une base SQLite en mémoire.
# StaticPool permet de garder la même base pendant toute la durée d'un test.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class FakeLLMResult:
    """Objet minimal qui imite le résultat retourné par l'agent IA."""

    def __init__(self, output="Réponse IA simulée"):
        self.output = output


def fake_agent_run_sync(*args, **kwargs):
    """Remplace l'appel réel au LLM par une réponse simulée."""
    return FakeLLMResult()


@pytest.fixture(autouse=True)
def isolate_external_services(monkeypatch):
    """
    Fixture lancée automatiquement avant chaque test.

    Objectif :
    - bloquer les appels réseau vers WorldNewsAPI ;
    - bloquer les vrais appels au LLM ;
    - rendre les tests rapides, stables et indépendants d'Internet.
    """
    import src.ai.conversationalAgent as agent_module
    import src.ai.todayNews as news_module

    class FakeNewsResponse:
        """Réponse factice qui imite une réponse HTTP de requests."""

        def raise_for_status(self):
            # Simule une réponse HTTP sans erreur.
            return None

        def json(self):
            # Simule une réponse vide de l'API d'actualités.
            return {"top_news": []}

    # Remplace requests.get par une fausse réponse.
    monkeypatch.setattr(
        news_module.requests,
        "get",
        lambda *args, **kwargs: FakeNewsResponse(),
    )

    # Remplace l'appel à l'agent IA par une fonction factice.
    monkeypatch.setattr(
        agent_module.agent,
        "run_sync",
        fake_agent_run_sync,
    )


@pytest.fixture(autouse=True)
def reset_database():
    """
    Fixture lancée automatiquement avant chaque test.

    Elle recrée une base propre pour éviter qu'un test influence un autre.
    """
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    # Ajoute un utilisateur de test présent par défaut dans la base.
    with Session(engine) as session:
        user = User(
            email="test@test.com",
            hashed_password=pwd_context.hash("test"),
        )
        session.add(user)
        session.commit()

    yield

    # Nettoie la base après le test.
    SQLModel.metadata.drop_all(engine)


def override_get_session():
    """
    Remplace la dépendance get_session de l'application.

    Au lieu d'utiliser la vraie base de données,
    FastAPI utilisera la base SQLite de test.
    """
    with Session(engine) as session:
        yield session


def override_user_1():
    """Simule un utilisateur connecté avec l'id 1."""
    return 1


def override_user_2():
    """Simule un utilisateur connecté avec l'id 2."""
    return 2


@pytest.fixture
def session():
    """
    Fournit une session SQLModel directement utilisable
    dans les tests unitaires.
    """
    with Session(engine) as session:
        yield session


@pytest.fixture
def client():
    """
    Fournit un client de test FastAPI.

    Les dépendances sont remplacées pour :
    - utiliser la base de données de test ;
    - simuler un utilisateur connecté.
    """
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user_id] = override_user_1

    with TestClient(app) as test_client:
        yield test_client

    # Supprime les overrides après le test pour éviter les effets de bord.
    app.dependency_overrides.clear()


@pytest.fixture
def as_user_2():
    """
    Permet à un test de simuler une connexion avec l'utilisateur 2.

    Utile pour tester l'isolation des données entre plusieurs utilisateurs.
    """
    app.dependency_overrides[get_current_user_id] = override_user_2

    yield

    # Remet l'utilisateur 1 comme utilisateur connecté par défaut.
    app.dependency_overrides[get_current_user_id] = override_user_1