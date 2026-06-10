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
                        "summary": summary.strip()
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


def build_news_system_prompt() -> str:
    """
    Construit le prompt système complet : base fixe + actualités du jour
    Appelé une seule fois à la création du chat, résultat sauvegardé en BDD.
    
    En cas d'erreur (API down, quota dépassé, clé manquante), on dégrade proprement : le chat fonctionne avec le prompt de base sans les news

    """

    return """
Tu es l'assistant IA de NewsFoundry.

Tu agis comme un rédacteur professionnel de revue de presse.

MISSION

Produire des synthèses d'actualité courtes, fiables et factuelles.

RÈGLES IMPORTANTES

- Utiliser uniquement les actualités fournies dans le contexte.
- Ne jamais utiliser des connaissances internes du modèle.
- Ne jamais inventer d'informations.
- Ne jamais inventer de dates.
- Ne jamais compléter avec des événements non fournis.
- Ne jamais mentionner :
  - "date de ma dernière mise à jour"
  - "selon mes connaissances"
  - "je recommande de consulter"
  - "sources"
  - "liens"
  - "pour en savoir plus"
- Ne jamais afficher d'URL.
- Ne jamais proposer de consulter un média.
- Ne jamais poser une question à la fin.
- Ne jamais ajouter de contenu extérieur aux actualités fournies.

STYLE

- Ton journalistique neutre.
- Phrases courtes.
- Informations essentielles uniquement.
- Regrouper les sujets similaires.

Tu dois répondre uniquement en Markdown

FORMAT OBLIGATOIRE

REVUE DE PRESSE - [DATE]

• Sujet :
Résumé court.

• Sujet :
Résumé court.

• Sujet :
Résumé court.

"""

def build_news_context() -> str:
    """
    Construit le contexte actualités.
    Appelé à chaque message du chat, doit être rapide à construire.
	- Récupérer les actualités du jour via l'API
	- Générer une synthèse courte
	- Formater le tout dans un contexte clair pour l'IA
    """

    today = date.today().strftime("%d/%m/%Y")

    try:
        articles = fetch_top_news()

        # 🔴 IMPORTANT : on utilise les vraies données ici
        formatted_articles = "\n\n".join(
            [
                f"- Titre : {a['title']}\n  Résumé : {a['summary']}"
                for a in articles[:8]
            ]
        )

        return f"""
DATE ACTUELLE : {today}

Tu ne connais aucune actualité en dehors de celles fournies.

Si l'information n'est pas présente :
Information non disponible dans les actualités fournies.

ACTUALITÉS DU JOUR :

{formatted_articles}
"""

    except Exception as e:
        print(f"[NewsFoundry] Erreur actualités : {e}")

        return f"""
DATE ACTUELLE : {today}

Aucune actualité disponible.
"""