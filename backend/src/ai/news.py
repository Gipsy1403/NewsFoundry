import os
import requests
from datetime import date
from src.ai.agent import agent

WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")
WORLD_NEWS_API_URL = "https://api.worldnewsapi.com/top-news"


def fetch_top_news() -> list[dict]:
    """
    Récupère les actualités du jour depuis World News API.
    Appelle le endpoint /top-news de World News API.
    Retourne une liste de dicts {"title": ..., "summary": ...}.
    On ne garde QUE titre + résumé, pas le texte complet (prompt plus court).

    """
    if not WORLD_NEWS_API_KEY:
        raise RuntimeError(
            "WORLD_NEWS_API_KEY manquante"
        )
    
    params = {
        "api-key": WORLD_NEWS_API_KEY,
        "source-country": "fr",
        "language": "fr",
        "date": str(date.today()),
        "headlines-only": "false",
    }

    response = requests.get(
        WORLD_NEWS_API_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    articles = []

# L'API retourne {"top_news": [{"news": [article, ...]}, ...]}
# Chaque "cluster" regroupe des articles sur un même sujet

    for cluster in data.get("top_news", []):
        for article in cluster.get("news", []):

            title = article.get("title", "").strip()

            summary = (
                article.get("summary")
                or article.get("text", "")[:250]
            ).strip()

            if title:
                articles.append(
                    {
                        "title": title,
                        "summary": summary.strip(),
                    #     "keywords": title.lower() + " " + summary.lower()
                    }
                )

    # Limiter le nombre d'articles
    return articles[:8]

def summarize_news(articles: list[dict]) -> str:
    """
    Génère une synthèse des actualités afin d'obtenir un prompt plus court.
    """

    if not articles:
        return "Aucune actualité disponible."

    articles_text = "\n\n".join(
        [
            (
                f"Titre : {article['title']}\n"
                f"Résumé : {article['summary']}"
            )
            for article in articles
        ]
    )

    prompt = f"""
Tu es journaliste.

Ta mission :

- regrouper les sujets similaires
- supprimer les redondances
- produire une synthèse concise
- maximum 10 lignes

Actualités :

{articles_text}
"""

    result = agent.run_sync(prompt)


    return result.output.strip()
# #     return result.output.strip()



def build_news_system_prompt(articles: list[dict]) -> str:
    """
    Construit le prompt système complet : base fixe + actualités du jour
    Appelé une seule fois à la création du chat, résultat sauvegardé en BDD.
    
    En cas d'erreur (API down, quota dépassé, clé manquante), on dégrade proprement : le chat fonctionne avec le prompt de base sans les news

    """

    articles_text = "\n\n".join(
        f"Titre : {a['title']}\nRésumé : {a['summary']}"
        for a in articles
    )

    summary = summarize_news(articles)

    return f"""
MISSION

Tu es un assistant spécialisé dans les actualités du jour.

Tu utilises uniquement les actualités fournies ci-dessous.

---

ACTUALITÉS BRUTES :
{articles_text}

---

SYNTHÈSE DES ACTUALITÉS :
{summary}

---

CAPACITÉS
- résumer
- comparer
- trier par thème
- revue de presse

CONTRAINTES
- utiliser uniquement les données fournies
- ne pas inventer d'informations
- ne pas utiliser de sources externes

STYLE
- journalistique
- neutre
- concis
"""
