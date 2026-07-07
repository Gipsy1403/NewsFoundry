import pytest
from src.ai import agent
from src.auth.dependencies import get_current_user_id
from src.main import app
from pydantic_ai.models.test import TestModel


# =========================
# TEST LLM
# =========================
class FakeResult:
    def __init__(self, output):
        self.output = output


def fake_run_sync(prompt):
    return FakeResult("Réponse IA simulée")


@pytest.fixture(autouse=True)
def mock_llm(monkeypatch):
    monkeypatch.setattr(agent, "run_sync", fake_run_sync)


# =========================
# Teste l'envoi d'un message dans une conversation
# =========================
def test_send_message(client):
#     remplace le vrai modèle d'IA par TestModel() pour simuler les réponses de l'IA
    with agent.override(
        model=TestModel()
    ):
     #    crée une nouvelle conversation via l'API FastAPI
        chat = client.post("/chats").json()

        chat_id = chat["chat_id"]
     #    envoie un message dans cette conversation
        response = client.post(
            f"/chats/{chat_id}/messages",
            json={
                "content": "Bonjour"
            }
        )
     #    Vérifie que la requête est correcte (code HTTP 200)
        assert response.status_code == 200

# =========================
# TEST HISTORIQUE
# =========================
def test_chat_history_persistence(client):
    chat = client.post("/chats").json()
    chat_id = chat["chat_id"]

    client.post(
        f"/chats/{chat_id}/messages",
        json={"content": "Hello"}
    )

    response = client.get(f"/chats/{chat_id}")

    assert response.status_code == 200

    messages = response.json()["messages"]

    roles = [m["role"] for m in messages]

    assert "user" in roles
    assert "assistant" in roles


# =========================
# Test pour vérifier qu'un utilisateur ne peut pas accéder à une conversation qui ne lui appartient pas
# =========================
def override_user_1():
    return 1


def override_user_2():
    return 2


def test_chat_access_forbidden(client):
    app.dependency_overrides[get_current_user_id] = override_user_1
#     crée une conversation pour l'utilisateur 1
    chat = client.post("/chats").json()

    chat_id = chat["chat_id"]

    app.dependency_overrides[get_current_user_id] = override_user_2
#   essaie d'accéder à la conversation de l'utilisateur 1 avec l'utilisateur 2
    response = client.get(f"/chats/{chat_id}")

    assert response.status_code == 403

    app.dependency_overrides.clear()
#     app.dependency_overrides = {}