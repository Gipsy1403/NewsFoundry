import requests
import src.ai.explorationTopic as ET


class DummySearchResponse:
    """
    Simule une réponse de l'API WorldNews.

    Permet de tester le code sans effectuer de véritables requêtes HTTP.
    """

    def __init__(self, data=None, raise_error=False):
        self.data = data or {}
        self.raise_error = raise_error

    def raise_for_status(self):
        """Simule une erreur HTTP si demandé."""
        if self.raise_error:
            raise requests.RequestException("Erreur API")

    def json(self):
        """Retourne les données simulées de l'API."""
        return self.data


def test_fetch_world_news_without_api_key_returns_empty_list(monkeypatch):
    """
    Vérifie qu'aucun appel API n'est effectué
    lorsqu'aucune clé API n'est configurée.
    """
    monkeypatch.setattr(ET, "WORLD_NEWS_API_KEY", None)

    result = ET.fetch_exploration_topic("bitcoin")

    assert result == []


def test_fetch_world_news_request_error_returns_empty_list(monkeypatch):
    """
    Vérifie qu'une erreur réseau est correctement gérée
    et qu'une liste vide est renvoyée.
    """
    monkeypatch.setattr(ET, "WORLD_NEWS_API_KEY", "key")

    def fake_get(*args, **kwargs):
        """Simule une erreur lors de la requête HTTP."""
        raise requests.RequestException("Erreur réseau")

    # Remplace requests.get par une version simulée.
    monkeypatch.setattr(ET.requests, "get", fake_get)

    result = ET.fetch_exploration_topic("bitcoin")

    assert result == []


def test_fetch_world_news_success_formats_articles(monkeypatch):
    """
    Vérifie que les articles retournés par l'API
    sont correctement filtrés et formatés.
    """
    monkeypatch.setattr(ET, "WORLD_NEWS_API_KEY", "key")

    # Réponse simulée de l'API.
    payload = {
        "news": [
            # Cet article doit être ignoré (titre vide).
            {"title": " ", "summary": "Article ignoré"},
            {
                "title": "Titre 1",
                "summary": "Résumé 1",
                "source_country": "FR",
                "publish_date": "2026-06-23T12:00:00",
            },
        ]
    }

    def fake_get(url, params=None, timeout=None):
        """
        Vérifie les paramètres envoyés à l'API
        puis retourne une réponse simulée.
        """
        assert params["number"] == 5
        assert timeout == 10

        return DummySearchResponse(payload)

    monkeypatch.setattr(ET.requests, "get", fake_get)

    result = ET.fetch_exploration_topic("q", max_results=5)

    # Seul l'article valide doit être conservé.
    assert result == [
        {
            "title": "Titre 1",
            "summary": "Résumé 1",
            "source": "FR",
            "date": "2026-06-23",
        }
    ]


def test_fetch_world_news_limits_max_results_between_1_and_10(monkeypatch):
    """
    Vérifie que le nombre de résultats demandés
    est limité entre 1 et 10.
    """
    monkeypatch.setattr(ET, "WORLD_NEWS_API_KEY", "key")

    # Stocke les valeurs réellement envoyées à l'API.
    observed_numbers = []

    def fake_get(url, params=None, timeout=None):
        observed_numbers.append(params["number"])
        return DummySearchResponse({"news": []})

    monkeypatch.setattr(ET.requests, "get", fake_get)

    # Valeur inférieure au minimum.
    ET.fetch_exploration_topic("q", max_results=0)

    # Valeur supérieure au maximum.
    ET.fetch_exploration_topic("q", max_results=99)

    # Les valeurs doivent être limitées à 1 et 10.
    assert observed_numbers == [1, 10]