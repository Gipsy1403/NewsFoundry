# créer un chat
def test_create_chat(client):
    response = client.post("/chats")

    assert response.status_code == 200
    data = response.json()

    assert "chat_id" in data

# Récupérer les chats
def test_get_chats(client):
    # créer chat
    client.post("/chats")

    response = client.get("/chats")

    assert response.status_code == 200
    assert isinstance(response.json(), list)