# # créer un chat
# def test_create_chat(client):
#     response = client.post("/chats")

#     assert response.status_code == 200
#     data = response.json()

#     assert "chat_id" in data

# # Récupérer les chats
# def test_get_chats(client):
#     # créer chat
#     client.post("/chats")

#     response = client.get("/chats")

#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

from src.main import app
from src.auth.dependencies import (
    get_current_user_id
)


def test_send_message(client):

    chat = client.post(
        "/chats"
    ).json()

    chat_id = chat["chat_id"]

    response = client.post(
        f"/chats/{chat_id}/messages",
        json={
            "content": "Bonjour"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["response"]
        == "Réponse IA simulée"
    )


def test_chat_history_persistence(client):

    chat = client.post(
        "/chats"
    ).json()

    chat_id = chat["chat_id"]

    client.post(
        f"/chats/{chat_id}/messages",
        json={
            "content": "Hello"
        }
    )

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


def test_chat_access_forbidden(client):

    chat = client.post(
        "/chats"
    ).json()

    chat_id = chat["chat_id"]

    app.dependency_overrides[
        get_current_user_id
    ] = override_user_2

    response = client.get(
        f"/chats/{chat_id}"
    )

    assert response.status_code == 403