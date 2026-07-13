from src.auth.dependencies import get_current_user_id
from src.main import app


def override_user_1():
    """Simule un utilisateur connecté avec l'id 1."""
    return 1


def override_user_2():
    """Simule un utilisateur connecté avec l'id 2."""
    return 2


def create_chat(client):
    """
    Crée un nouveau chat via l'API et retourne son identifiant.

    Cette fonction évite de répéter le même code dans plusieurs tests.
    """
    response = client.post("/chats")

    # La création du chat doit réussir.
    assert response.status_code == 200

    chat = response.json()

    # Compatibilité si l'API retourne "id" ou "chat_id".
    chat_id = chat.get("id") or chat.get("chat_id")

    assert chat_id is not None

    return chat_id


def test_user_can_create_chat(client):
    """
    Vérifie qu'un utilisateur connecté peut créer un chat.
    """
    chat_id = create_chat(client)

    # L'identifiant du chat doit être un entier.
    assert isinstance(chat_id, int)


def test_user_can_access_own_chat(client):
    """
    Vérifie qu'un utilisateur peut consulter son propre chat.
    """
    chat_id = create_chat(client)

    response = client.get(f"/chats/{chat_id}")

    assert response.status_code == 200
    assert response.json()["id"] == chat_id


def test_user_can_send_message_to_own_chat(client):
    """
    Vérifie qu'un utilisateur peut envoyer un message
    dans son propre chat.
    """
    chat_id = create_chat(client)

    response = client.post(
        f"/chats/{chat_id}/messages",
        json={"content": "Bonjour"},
    )

    assert response.status_code == 200

    data = response.json()

    # La réponse de l'IA doit être présente.
    assert "response" in data

    # Le chat doit contenir un message utilisateur
    # puis une réponse de l'assistant.
    assert len(data["chat"]) == 2
    assert data["chat"][0]["role"] == "user"
    assert data["chat"][1]["role"] == "assistant"


def test_chat_history_is_persisted(client):
    """
    Vérifie que l'historique des messages est bien
    enregistré en base de données.
    """
    chat_id = create_chat(client)

    client.post(
        f"/chats/{chat_id}/messages",
        json={"content": "Hello"},
    )

    response = client.get(f"/chats/{chat_id}")

    assert response.status_code == 200

    messages = response.json()["messages"]
    roles = [message["role"] for message in messages]

    # Les deux messages doivent être retrouvés dans l'ordre.
    assert roles == ["user", "assistant"]


def test_user_cannot_read_another_user_chat(client):
    """
    Vérifie qu'un utilisateur ne peut pas consulter
    le chat appartenant à un autre utilisateur.
    """
    # L'utilisateur 1 crée un chat.
    app.dependency_overrides[get_current_user_id] = override_user_1
    chat_id = create_chat(client)

    # L'utilisateur 2 tente d'y accéder.
    app.dependency_overrides[get_current_user_id] = override_user_2

    response = client.get(f"/chats/{chat_id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Accès interdit"


def test_user_cannot_modify_another_user_chat(client):
    """
    Vérifie qu'un utilisateur ne peut pas ajouter
    de messages dans le chat d'un autre utilisateur.
    """
    # L'utilisateur 1 crée un chat.
    app.dependency_overrides[get_current_user_id] = override_user_1
    chat_id = create_chat(client)

    # L'utilisateur 2 tente de modifier ce chat.
    app.dependency_overrides[get_current_user_id] = override_user_2

    response = client.post(
        f"/chats/{chat_id}/messages",
        json={"content": "Je tente de modifier ce chat"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Accès interdit"


def test_unknown_chat_returns_404(client):
    """
    Vérifie que la consultation d'un chat inexistant
    renvoie une erreur 404.
    """
    response = client.get("/chats/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat introuvable"


def test_create_chat_handles_news_fetch_error(client, monkeypatch):
    """
    Simule une erreur lors de la récupération des actualités
    et vérifie que la création de chat renvoie un 500.
    """
    import src.routes.chats as chats_module

    def fake_fetch():
        raise Exception("Service d'actualités indisponible")

    # Remplace la fonction de récupération des actualités
    monkeypatch.setattr(chats_module, "fetch_top_news_today_news", fake_fetch)

    response = client.post("/chats")

    assert response.status_code == 500
    assert response.json()["detail"] == "Erreur lors de la création du chat"