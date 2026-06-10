from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from src.ai.tools import search_news as _search_news

model = MistralModel("mistral-small")

agent = Agent(model)


# Tool : recherche d'articles sur un sujet
@agent.tool_plain
def search_news(query: str, max_results: int = 5) -> str:
    """
    Recherche des articles d'actualité sur le sujet demandé par l'utilisateur.

    Utilise cet outil quand l'utilisateur veut approfondir un sujet,
    obtenir plus d'informations ou explorer un thème précis.

    Paramètres
    ----------
    query       : sujet ou mots-clés à rechercher (en français de préférence)
    max_results : nombre d'articles souhaités (entre 1 et 10, défaut 5)

    Retour
    ------
    Résumé textuel des articles trouvés, prêt à être utilisé dans ta réponse.
    """

    try:
        articles = _search_news(query=query, max_results=max_results)

        if not articles:
            return f"Aucun article trouvé pour le sujet : « {query} »."

        lines = [f"Résultats de recherche pour « {query} » ({len(articles)} articles) :\n"]

        for i, art in enumerate(articles, start=1):
            lines.append(f"{i}. {art['title']} ({art['date']})")
            if art["summary"]:
                lines.append(f"   {art['summary']}")

        return "\n".join(lines)

    except Exception as e:
        return f"Erreur lors de la recherche d'articles : {e}"
