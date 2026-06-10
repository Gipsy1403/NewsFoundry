import os
import requests
from pydantic_ai import RunContext

WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")
WORLD_NEWS_SEARCH_URL = "https://api.worldnewsapi.com/search-news"


def search_news(query: str, max_results: int = 5) -> list[dict]:
    """
    Tool exposé à l'agent : recherche des articles sur un sujet précis.

    Paramètres
    ----------
    query       : mots-clés de recherche (ex. "intelligence artificielle")
    max_results : nombre maximum d'articles retournés (1-10)

    Retour
    ------
    Liste de dicts simples :  {"title": ..., "summary": ..., "source": ..., "date": ...}
    Format volontairement minimal pour ne pas polluer la fenêtre de contexte du LLM.
    """

    max_results = max(1, min(max_results, 10))  # borne 1-10

    params = {
        "api-key": WORLD_NEWS_API_KEY,
        "text": query,
        "language": "fr",
        "number": max_results,
        "sort": "publish-time",
        "sort-direction": "DESC",
    }

    response = requests.get(
        WORLD_NEWS_SEARCH_URL,
        params=params,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    articles = []
    for article in data.get("news", []):
        title = article.get("title", "").strip()
        if not title:
            continue

        summary = (
            article.get("summary")
            or article.get("text", "")[:300]
        ).strip()

        articles.append({
            "title": title,
            "summary": summary,
            # Nom du site source (utile pour créditer sans exposer d'URL)
            "source": article.get("source_country", ""),
            "date": (article.get("publish_date") or "")[:10],  # YYYY-MM-DD
        })

    return articles
