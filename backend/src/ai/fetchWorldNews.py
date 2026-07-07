import os
import requests

WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")
WORLD_NEWS_SEARCH_URL = "https://api.worldnewsapi.com/search-news"


def fetch_world_news(query: str, max_results: int = 5) -> list[dict]:
    """
    Recherche des articles récents sur un sujet.
    Retourne un format simplifié pour faciliter l'utilisation par le LLM.
    """
    if not WORLD_NEWS_API_KEY: return []

    max_results = max(1, min(max_results, 10))

    params = {
        "api-key": WORLD_NEWS_API_KEY,
        "text": query,
        "language": "fr",
        "number": max_results,
        "sort": "publish-time",
        "sort-direction": "DESC",
    }
    try:
       response = requests.get(
           WORLD_NEWS_SEARCH_URL,
           params=params,
           timeout=10,
       )
       response.raise_for_status()

       data = response.json()
       
    except requests.RequestException:
        return []

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


