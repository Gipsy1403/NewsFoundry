import types
import pytest

import src.ai.news as news


def test_fetch_top_news_missing_key(monkeypatch):
    monkeypatch.setattr(news, "WORLD_NEWS_API_KEY", None)
    with pytest.raises(RuntimeError):
        news.fetch_top_news()


def test_summarize_news_empty():
    assert news.summarize_news([]) == "Aucune actualité disponible."


def test_summarize_news_calls_agent(monkeypatch):
    # Simule l'agent pour retourner une sortie prévisible
    class Out:
        def __init__(self, output):
            self.output = output

    def fake_run_sync(prompt):
        return Out("Synthèse générée")

    monkeypatch.setattr(news.agent, "run_sync", fake_run_sync)

    articles = [{"title": "T1", "summary": "S1"}]
    res = news.summarize_news(articles)
    assert res == "Synthèse générée"


def test_build_news_system_prompt_includes_summary(monkeypatch):
    # On remplace summarize_news pour contrôle
    monkeypatch.setattr(news, "summarize_news", lambda articles: "RES_SUM")
    articles = [{"title": "T1", "summary": "S1"}]
    prompt = news.build_news_system_prompt(articles)
    assert "RES_SUM" in prompt
    assert "Titre : T1" in prompt
