import types
import requests

import src.ai.fetchWorldNews as fw


class DummyResponse:
    def __init__(self, data=None, raise_exc=False):
        self._data = data or {}
        self._raise = raise_exc

    def raise_for_status(self):
        if self._raise:
            raise requests.RequestException("fail")

    def json(self):
        return self._data


def test_fetch_world_news_no_api_key(monkeypatch):
    monkeypatch.setattr(fw, "WORLD_NEWS_API_KEY", None)
    res = fw.fetch_world_news("bitcoin")
    assert res == []


def test_fetch_world_news_request_exception(monkeypatch):
    monkeypatch.setattr(fw, "WORLD_NEWS_API_KEY", "key")

    def fake_get(*args, **kwargs):
        raise requests.RequestException()

    monkeypatch.setattr(fw.requests, "get", fake_get)

    res = fw.fetch_world_news("query")
    assert res == []


def test_fetch_world_news_success(monkeypatch):
    monkeypatch.setattr(fw, "WORLD_NEWS_API_KEY", "key")

    data = {
        "news": [
            {"title": "  ", "summary": "no title"},
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
