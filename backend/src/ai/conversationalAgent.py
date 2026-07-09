from pydantic_ai import Agent, RunContext
from pydantic_ai.models.mistral import MistralModel
from datetime import date
from src.ai.explorationTopic import fetch_exploration_topic 


model = MistralModel("mistral-small")


agent = Agent(
    model,
    deps_type=str,
    output_type=str,
    system_prompt="""
Tu es NewsFoundry, un assistant spécialisé dans l'analyse et la synthèse d'actualités.

Pour toute question relative à la date actuelle, au jour actuel, au mois actuel ou à l'année en cours, utilise l'outil current_date.

Quand l'utilisateur souhaite :

- approfondir un sujet,
- obtenir davantage d'informations,
- explorer une actualité,
- rechercher des articles récents,

utilise l'outil search_news.

Base tes réponses sur les articles récupérés.

Lorsque plusieurs articles sont trouvés :
- identifie les points communs,
- résume les informations importantes,
- cite les titres lorsque c'est pertinent.

"""
)

@agent.system_prompt
def add_chat_context(ctx: RunContext[str]) -> str:
    """
    Ajoute le contexte spécifique au chat (actualités du jour),
    généré une fois à la création du chat et stocké en BDD.
    """
    return ctx.deps or ""


@agent.tool_plain
def search_news(
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """
Recherche des articles récents sur un sujet.
Retourne un format simplifié...
    """

    return fetch_exploration_topic(
        query=query,
        max_results=max_results,
    )


@agent.tool_plain
def current_date() -> str:
    """Retourne la date du jour."""
    return date.today().strftime("%d/%m/%Y")
