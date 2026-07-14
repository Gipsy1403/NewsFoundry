# import os
# import requests
# from datetime import date
# from src.ai.conversationalAgent import agent

# WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")
# WORLD_NEWS_API_URL = "https://api.worldnewsapi.com/top-news"

# # ---------------------------------------------------
# # Récupération des actualités du jour sur WorldNews API

# def fetch_top_news_today_news() -> list[dict]:
#     """
#     Récupère les actualités du jour depuis World News API.
#     Appelle le endpoint /top-news de World News API.
#     Retourne une liste de dicts {"title": ..., "summary": ...}.
#     On ne garde QUE titre + résumé, pas le texte complet (prompt plus court).

#     """
#     if not WORLD_NEWS_API_KEY:
#         raise RuntimeError(
#             "WORLD_NEWS_API_KEY manquante"
#         )
    
#     params = {
#         "api-key": WORLD_NEWS_API_KEY,
#         "source-country": "fr",
#         "language": "fr",
#         "date": str(date.today()),
#         "headlines-only": "false",
#     }

#     response = requests.get(
#         WORLD_NEWS_API_URL,
#         params=params,
#         timeout=10,
#     )

#     response.raise_for_status()

#     data = response.json()

#     articles = []

# # L'API retourne {"top_news": [{"news": [article, ...]}, ...]}
# # Chaque "cluster" regroupe des articles sur un même sujet

#     for cluster in data.get("top_news", []):
#         for article in cluster.get("news", []):

#             title = article.get("title", "").strip()

#             summary = (
#                 article.get("summary")
#                 or article.get("text", "")[:250]
#             ).strip()

#             if title:
#                 articles.append(
#                     {
#                         "title": title,
#                         "summary": summary.strip(),
#                     }
#                 )

#     # Limiter le nombre d'articles
#     return articles[:8]

# # --------------------------------------------------
# # Résume les actualités

# def summarize_today_news(articles: list[dict]) -> str:
#     """
#     Génère une synthèse des actualités afin d'obtenir un prompt plus court.
#     """

#     if not articles:
#         return "Aucune actualité disponible."

#     articles_text = "\n\n".join(
#         [
#             (
#                 f"Titre : {article['title']}\n"
#                 f"Résumé : {article['summary']}"
#             )
#             for article in articles
#         ]
#     )

#     prompt = f"""
# Tu es journaliste.

# Ta mission :

# - regrouper les sujets similaires
# - supprimer les redondances
# - produire une synthèse concise
# - maximum 10 lignes

# Actualités :

# {articles_text}
# """

#     result = agent.run_sync(prompt)


#     return result.output.strip()


# # ----------------------------------------------------------
# # Construit le prompt système complet qui sera envoyé à l'IA en y intégrant les actualités du jour et leur synthèse

# def build_today_news_prompt(articles: list[dict]) -> str:
#     """
#     Construit le prompt système complet : base fixe + actualités du jour
#     Appelé une seule fois à la création du chat, résultat sauvegardé en BDD.

#     """

#     articles_text = "\n\n".join(
#         f"Titre : {a['title']}\nRésumé : {a['summary']}"
#         for a in articles
#     )

#     summary = summarize_today_news(articles)

#     return f"""
# MISSION

# Tu es un assistant spécialisé dans les actualités du jour.

# Tu utilises uniquement les actualités fournies ci-dessous.

# ---

# ACTUALITÉS BRUTES :
# {articles_text}

# ---

# SYNTHÈSE DES ACTUALITÉS :
# {summary}

# ---

# CAPACITÉS
# - résumer
# - comparer
# - trier par thème
# - revue de presse

# CONTRAINTES
# - utiliser uniquement les données fournies
# - ne pas inventer d'informations
# - ne pas utiliser de sources externes

# STYLE
# - journalistique
# - neutre
# - concis
# """

import os
import requests
from datetime import date
from src.ai.conversationalAgent import agent

WORLD_NEWS_API_KEY = os.getenv("WORLD_NEWS_API_KEY")
WORLD_NEWS_API_URL = "https://api.worldnewsapi.com/top-news"

# ---------------------------------------------------
# Récupération des actualités du jour sur WorldNews API

def fetch_top_news_today_news() -> list[dict]:
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
                    }
                )

    # Limiter le nombre d'articles
    return articles[:8]

# --------------------------------------------------
# Résume les actualités

def summarize_today_news(articles: list[dict]) -> str:
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


# ----------------------------------------------------------
# Construit le prompt système complet qui sera envoyé à l'IA en y intégrant les actualités du jour et leur synthèse

def build_today_news_prompt(articles: list[dict]) -> str:
    """
    Construit le contexte d'actualités propre à un nouveau chat.

    Ce texte est généré une seule fois lors de la création du chat,
    puis il est enregistré en base de données dans ``chat.context``.
    """

    if not articles:
        articles_text = "Aucune actualité brute disponible."
    else:
        articles_text = "\n\n".join(
            f"Titre : {article['title']}\nRésumé : {article['summary']}"
            for article in articles
        )

    summary = summarize_today_news(articles)

    return f"""
CONTEXTE D'ACTUALITÉS DU CHAT

Les informations ci-dessous ont été récupérées lors de la création du chat.
Utilise-les en priorité pour répondre aux questions de l'utilisateur.

---

ACTUALITÉS BRUTES

{articles_text}

---

SYNTHÈSE DES ACTUALITÉS

{summary}

---

CAPACITÉS ATTENDUES
- résumer les actualités ;
- comparer plusieurs articles ;
- regrouper les informations par thème ;
- produire une revue de presse ;
- expliquer les points essentiels de façon claire.

RÈGLES D'UTILISATION DU CONTEXTE
- appuie-toi d'abord sur les informations fournies ci-dessus ;
- n'invente aucune information absente des données disponibles ;
- signale clairement lorsqu'une information n'est pas présente dans ce contexte ;
- utilise l'outil search_news seulement si une recherche complémentaire est nécessaire selon les règles générales de l'agent ;
- lorsque search_news est utilisé, distingue les nouveaux résultats du contexte initial du chat.
""".strip()