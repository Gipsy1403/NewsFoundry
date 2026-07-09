from src.ai.convertHistoryForPydantic import convert_history_for_pydantic


def test_build_history_converts_user_and_assistant_messages():
    """
    Vérifie que les messages de l'utilisateur et de l'assistant
    sont correctement convertis au format attendu par PydanticAI.
    """
    # Historique de conversation simulé.
    messages = [
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Bonjour, comment puis-je aider ?"},
    ]

    # Conversion vers les objets utilisés par PydanticAI.
    history = convert_history_for_pydantic(messages)

    # Deux messages doivent être présents après la conversion.
    assert len(history) == 2

    # Vérifie que le contenu du message utilisateur est conservé.
    assert history[0].parts[0].content == "Bonjour"

    # Vérifie que le contenu de la réponse de l'assistant est conservé.
    assert history[1].parts[0].content == "Bonjour, comment puis-je aider ?"