import pytest
from src.ai import agent
from src.auth.dependencies import get_current_user_id
from src.main import app
from pydantic_ai.models.test import TestModel


# =========================
# MOCK LLM
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
# TEST CHAT MESSAGE
# =========================
def test_send_message(client):

    with agent.override(
        model=TestModel()
    ):

        chat = client.post("/chats").json()

        chat_id = chat["chat_id"]

        response = client.post(
            f"/chats/{chat_id}/messages",
            json={
                "content": "Bonjour"
            }
        )

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
# TEST SÉCURITÉ
# =========================
def override_user_1():
    return 1


def override_user_2():
    return 2


def test_chat_access_forbidden(client):
    chat = client.post("/chats").json()
    chat_id = chat["chat_id"]

    app.dependency_overrides[get_current_user_id] = override_user_2

    response = client.get(f"/chats/{chat_id}")

    assert response.status_code == 403

    app.dependency_overrides = {}