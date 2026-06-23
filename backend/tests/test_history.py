from src.ai.history import build_history


def test_build_history_basic():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]

    history = build_history(messages)
    assert len(history) == 2
    # Chaque élément doit exposer des 'parts' contenant le texte original
    assert history[0].parts[0].content == "Hello"
    assert history[1].parts[0].content == "Hi"
