import pytest

import src.ai.news as news

# simule l'absence de la clé d'API pour tester le comportement de la fonction fetch_top_news()
def test_fetch_top_news_missing_key(monkeypatch):
    monkeypatch.setattr(news, "WORLD_NEWS_API_KEY", None)
    with pytest.raises(RuntimeError):
        news.fetch_top_news()

# vérifie que la fonction retourne un message lorsque la liste d'articles est vide
def test_summarize_news_empty():
    assert news.summarize_news([]) == "Aucune actualité disponible."

# simule la réponse de l'agent IA pour vérifier que la fonction summarize_news() l'utilise correctement
def test_summarize_news_calls_agent(monkeypatch):

    class Out:
        def __init__(self, output):
          #   stocke le texte que l'IA est censée générer pour la synthèse des articles
            self.output = output

    def fake_run_sync(prompt):
        return Out("Synthèse générée")

    monkeypatch.setattr(news.agent, "run_sync", fake_run_sync)

    articles = [{"title": "T1", "summary": "S1"}]
    res = news.summarize_news(articles)
    assert res == "Synthèse générée"

# remplace summarize_news() pour contrôler le résultat et vérifier que build_news_system_prompt() l'utilise correctement
def test_build_news_system_prompt_includes_summary(monkeypatch):

    monkeypatch.setattr(news, "summarize_news", lambda articles: "RES_SUM")
    articles = [{"title": "T1", "summary": "S1"}]
    prompt = news.build_news_system_prompt(articles)
    assert "RES_SUM" in prompt
    assert "Titre : T1" in prompt
