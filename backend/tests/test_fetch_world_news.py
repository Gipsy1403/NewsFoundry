import types
import requests

import src.ai.fetchWorldNews as fw


class DummyResponse:
    def __init__(self, data=None, raise_exc=False):
     #    données JSON qui seront renvoyées par json()
        self._data = data or {}
     #    indique si une exception doit être levée lors de l'appel à raise_for_status()
        self._raise = raise_exc

    def raise_for_status(self):
     #    simule une erreur HTTP si _raise est True, sinon ne fait rien
        if self._raise:
            raise requests.RequestException("fail")

    def json(self):
     #    retourne les données JSON simulées
        return self._data

# --------------------------------
# simule l'absence de clé API
def test_fetch_world_news_no_api_key(monkeypatch):
    monkeypatch.setattr(fw, "WORLD_NEWS_API_KEY", None)
#     appelle la fonction fetch_world_news() avec un mot-clé de recherche et vérifie que le résultat est une liste vide
    res = fw.fetch_world_news("bitcoin")
    assert res == []

# --------------------------------
# simule une clé API valide mais une exception de requête pour tester le comportement de la fonction fetch_world_news()
def test_fetch_world_news_request_exception(monkeypatch):
    monkeypatch.setattr(fw, "WORLD_NEWS_API_KEY", "key")

    def fake_get(*args, **kwargs):
        raise requests.RequestException()

    monkeypatch.setattr(fw.requests, "get", fake_get)
# appelle la fonction fetch_world_news() et vérifie que le résultat est une liste vide en cas d'exception de requête
    res = fw.fetch_world_news("query")
    assert res == []

# --------------------------------
# simule une clé API valide et une réponse JSON contenant des articles pour tester le comportement de la fonction fetch_world_news() en cas de succès
def test_fetch_world_news_success(monkeypatch):
    monkeypatch.setattr(fw, "WORLD_NEWS_API_KEY", "key")

    data = {
        "news": [
            {"title": "  ", "summary": "no title"}, # article avec titre vide, devrait être ignoré
            {"title": "Titre 1", "summary": "Résumé 1", "source_country": "FR", "publish_date": "2026-06-23T12:00:00"},
        ]
    }

    def fake_get(url, params=None, timeout=None):
        return DummyResponse(data=data)

    monkeypatch.setattr(fw, "requests", types.SimpleNamespace(get=fake_get))

    res = fw.fetch_world_news("q", max_results=5)
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]["title"] == "Titre 1"
