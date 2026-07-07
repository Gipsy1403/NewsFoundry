from src.main import app
from src.auth.dependencies import (
    get_current_user_id
)

# vérifie qu'un utilisateur peut envoyer un message dans une conversation et que l'IA répond correctement
def test_send_message(client):
#  crée une nouvelle conversation via l'API FastAPI
    chat = client.post(
        "/chats"
    ).json()
# récupère l'identifiant de la conversation créée
    chat_id = chat.get("chat_id") or chat.get("id")
#     vérifie que l'identifiant existe
    assert chat_id is not None

    response = client.post(
        f"/chats/{chat_id}/messages",
        json={
            "content": "Bonjour"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0

# vérifie que les message s sont correctement stockés et récupérés dans l'historique de la conversation
def test_chat_history_persistence(client):

    chat = client.post(
        "/chats"
    ).json()

    chat_id = chat.get("chat_id") or chat.get("id")
    assert chat_id is not None
#   envoie un message dans cette conversation
    client.post(
        f"/chats/{chat_id}/messages",
        json={
            "content": "Hello"
        }
    )
# récupère la conversation entière
    response = client.get(
        f"/chats/{chat_id}"
    )

    assert response.status_code == 200

    messages = response.json()["messages"]

    roles = [
        m["role"]
        for m in messages
    ]

    assert "user" in roles
    assert "assistant" in roles


def override_user_2():
    return 2

# vérifie qu'un utilisateur ne peut pas accéder à une conversation qui ne lui appartient pas
def test_chat_access_forbidden(client):

    chat = client.post(
        "/chats"
    ).json()

    chat_id = chat.get("chat_id") or chat.get("id")
    assert chat_id is not None

    app.dependency_overrides[
        get_current_user_id
    ] = override_user_2

    response = client.get(
        f"/chats/{chat_id}"
    )

    assert response.status_code == 403