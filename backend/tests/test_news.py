import pytest
import src.ai.todayNews as news


class DummyTopNewsResponse:
    """
    Simule une réponse de l'API WorldNews.

    Permet de tester les fonctions sans effectuer
    de véritables appels HTTP.
    """

    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        """Simule une réponse HTTP sans erreur."""
        return None

    def json(self):
        """Retourne les données simulées."""
        return self.data


def test_fetch_top_news_today_news_missing_key(monkeypatch):
    """
    Vérifie qu'une exception est levée lorsqu'aucune
    clé API n'est configurée.
    """
    monkeypatch.setattr(news, "WORLD_NEWS_API_KEY", None)

    with pytest.raises(RuntimeError):
        news.fetch_top_news_today_news()


def test_fetch_top_news_today_news_keeps_title_and_summary(monkeypatch):
    """
    Vérifie que les articles récupérés sont correctement
    filtrés et formatés.
    """
    monkeypatch.setattr(news, "WORLD_NEWS_API_KEY", "key")

    # Réponse simulée de l'API.
    payload = {
        "top_news": [
            {
                "news": [
                    {
                        "title": "Titre 1",
                        "summary": "Résumé 1",
                    },
                    # Doit être ignoré car le titre est vide.
                    {
                        "title": " ",
                        "summary": "Sans titre",
                    },
                    # Si le résumé est absent, le texte est utilisé.
                    {
                        "title": "Titre 2",
                        "text": "Texte long de secours",
                    },
                ]
            }
        ]
    }

    # Remplace l'appel HTTP par une réponse simulée.
    monkeypatch.setattr(
        news.requests,
        "get",
        lambda *args, **kwargs: DummyTopNewsResponse(payload),
    )

    articles = news.fetch_top_news_today_news()

    # Seuls les articles valides doivent être conservés.
    assert articles == [
        {"title": "Titre 1", "summary": "Résumé 1"},
        {"title": "Titre 2", "summary": "Texte long de secours"},
    ]


def test_summarize_news_empty_list():
    """
    Vérifie qu'un message par défaut est renvoyé
    lorsqu'il n'y a aucune actualité à résumer.
    """
    assert news.summarize_today_news([]) == "Aucune actualité disponible."


def test_summarize_today_news_calls_llm(monkeypatch):
    """
    Vérifie que les actualités sont bien transmises
    au LLM et que sa réponse est renvoyée.
    """

    class Result:
        output = "Synthèse générée"

    def fake_run_sync(prompt):
        # Vérifie que le prompt contient les informations attendues.
        assert "Titre : T1" in prompt
        assert "Résumé : S1" in prompt

        return Result()

    # Remplace l'appel au LLM par une fonction simulée.
    monkeypatch.setattr(news.agent, "run_sync", fake_run_sync)

    result = news.summarize_today_news(
        [
            {
                "title": "T1",
                "summary": "S1",
            }
        ]
    )

    assert result == "Synthèse générée"


def test_build_news_system_prompt_contains_raw_articles_and_summary(monkeypatch):
    """
    Vérifie que le prompt final contient :
    - les actualités brutes ;
    - la synthèse générée.
    """
    # Remplace la synthèse réelle par une valeur fixe.
    monkeypatch.setattr(
        news,
        "summarize_today_news",
        lambda articles: "Synthèse courte",
    )

    prompt = news.build_today_news_prompt(
        [
            {
                "title": "T1",
                "summary": "S1",
            }
        ]
    )

    # Vérifie la structure du prompt.
    assert "ACTUALITÉS BRUTES" in prompt
    assert "Titre : T1" in prompt
    assert "Résumé : S1" in prompt
    assert "SYNTHÈSE DES ACTUALITÉS" in prompt
    assert "Synthèse courte" in prompt