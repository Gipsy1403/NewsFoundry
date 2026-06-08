# backend/src/ai/news.py

import os
import requests
from datetime import date

WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")
WORLD_NEWS_API_URL = "https://api.worldnewsapi.com/top-news"


def fetch_top_news() -> list[dict]:
    """
    Appelle le endpoint /top-news de World News API.
    Retourne une liste de dicts {"title": ..., "summary": ...}.
    On ne garde QUE titre + résumé, pas le texte complet (prompt plus court).
    """
    params = {
        "api-key": WORLD_NEWS_API_KEY,
        "source-country": "fr",
        "language": "fr",
        "date": str(date.today()),
        "headlines-only": "false",
    }

    response = requests.get(WORLD_NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    articles = []
    # L'API retourne {"top_news": [{"news": [article, ...]}, ...]}
    # Chaque "cluster" regroupe des articles sur un même sujet
    for cluster in data.get("top_news", []):
        for article in cluster.get("news", []):
            title = article.get("title", "").strip()
            # "summary" n'existe pas toujours → on tronque le texte à 200 caractères
            summary = article.get("summary") or article.get("text", "")[:200]
            if title:
                articles.append({"title": title, "summary": summary.strip()})

    return articles


def build_news_system_prompt() -> str:
    """
    Construit le prompt système complet : base fixe + actualités du jour.
    Appelé une seule fois à la création du chat, résultat sauvegardé en BDD.

    En cas d'erreur (API down, quota dépassé, clé manquante), on dégrade
    proprement : le chat fonctionne avec le prompt de base sans les news.
    """

    base_prompt = """Tu es l'assistant IA de NewsFoundry.

Ta mission est d'aider les utilisateurs à :
- comprendre l'actualité,
- analyser des articles,
- résumer des informations,
- identifier les points importants d'un sujet.

Règles :
- répondre de manière claire et professionnelle ;
- utiliser un langage accessible ;
- structurer les réponses avec des titres et listes lorsque cela améliore la lisibilité ;
- signaler lorsqu'une information est incertaine ;
- ne jamais inventer de faits."""

    try:
        articles = fetch_top_news()

        if not articles:
            print("[NewsFoundry] Aucun article retourné par l'API.")
            return base_prompt

        # On formate : "1. Titre\n   Résumé : ..."
        lines = []
        for i, article in enumerate(articles, 1):
            lines.append(f"{i}. {article['title']}")
            if article["summary"]:
                lines.append(f"   Résumé : {article['summary']}")

        news_text = "\n".join(lines)
        today = date.today().strftime("%d/%m/%Y")

        full_prompt = f"""{base_prompt}

---

## Actualités du jour ({today})

Tu disposes ci-dessous des principales actualités du jour.
Utilise ces informations pour répondre aux questions sur l'actualité récente.
Si une question ne concerne pas ces actualités, réponds normalement.

{news_text}"""

        return full_prompt

    except Exception as e:
        # Dégradation propre : le chat fonctionne quand même sans les news
        print(f"[NewsFoundry] Impossible de récupérer les actualités : {e}")
        return base_prompt