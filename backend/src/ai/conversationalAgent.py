# from pydantic_ai import Agent, RunContext
# from pydantic_ai.models.mistral import MistralModel
# from datetime import date
# from src.ai.explorationTopic import fetch_exploration_topic 


# model = MistralModel("mistral-small")


# agent = Agent(
#     model,
#     deps_type=str,
#     output_type=str,
#     system_prompt="""
# Tu es NewsFoundry, un assistant spécialisé dans l'analyse et la synthèse d'actualités.

# Pour toute question relative à la date actuelle, au jour actuel, au mois actuel ou à l'année en cours, utilise l'outil current_date.

# Quand l'utilisateur souhaite :

# - approfondir un sujet,
# - obtenir davantage d'informations,
# - explorer une actualité,
# - rechercher des articles récents,

# utilise l'outil search_news.

# Base tes réponses sur les articles récupérés.

# Lorsque plusieurs articles sont trouvés :
# - identifie les points communs,
# - résume les informations importantes,
# - cite les titres lorsque c'est pertinent.

# """
# )

# @agent.system_prompt
# def add_chat_context(ctx: RunContext[str]) -> str:
#     """
#     Ajoute le contexte spécifique au chat (actualités du jour),
#     généré une fois à la création du chat et stocké en BDD.
#     """
#     return ctx.deps or ""


# @agent.tool_plain
# def search_news(
#     query: str,
#     max_results: int = 5,
# ) -> list[dict]:
#     """
# Recherche des articles récents sur un sujet.
# Retourne un format simplifié...
#     """

#     return fetch_exploration_topic(
#         query=query,
#         max_results=max_results,
#     )


# @agent.tool_plain
# def current_date() -> str:
#     """Retourne la date du jour."""
#     return date.today().strftime("%d/%m/%Y")


from datetime import date

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.mistral import MistralModel

from src.ai.explorationTopic import fetch_exploration_topic


# Modèle de langage utilisé par l'agent conversationnel.
model = MistralModel("mistral-small")


agent = Agent(
    model,
    # Le contexte ajouté à chaque chat est une chaîne de caractères.
    deps_type=str,
    # La réponse finale attendue est du texte.
    output_type=str,
    system_prompt="""
Tu es NewsFoundry, un assistant spécialisé dans l'analyse et la synthèse d'actualités.

RÈGLES GÉNÉRALES
- Réponds en français.
- Adopte un style journalistique, neutre, clair et concis.
- N'invente jamais une information, une source, un titre ou une citation.
- Distingue clairement les informations présentes dans le contexte du chat des résultats obtenus par une recherche complémentaire.

DATE ACTUELLE
Pour toute question relative à la date actuelle, au jour actuel, au mois actuel ou à l'année en cours, utilise l'outil current_date.

CONTEXTE DU CHAT
Un contexte d'actualités peut être ajouté au prompt système lors de l'exécution.
Utilise d'abord ce contexte pour répondre à l'utilisateur.

RECHERCHE COMPLÉMENTAIRE
Utilise l'outil search_news uniquement lorsque :
- l'utilisateur demande explicitement d'approfondir un sujet ;
- l'utilisateur souhaite obtenir davantage d'informations ;
- l'utilisateur veut explorer une actualité ;
- l'utilisateur demande des articles récents ;
- l'information demandée n'est pas présente dans le contexte du chat ;
- l'utilisateur demande une mise à jour plus récente que le contexte disponible.

Lorsque tu utilises search_news :
- base ta réponse sur les articles réellement récupérés ;
- indique qu'il s'agit d'une recherche complémentaire ;
- identifie les points communs entre les articles ;
- résume les informations importantes ;
- cite les titres des articles lorsque c'est pertinent.
""",
)


@agent.system_prompt
def add_chat_context(ctx: RunContext[str]) -> str:
    """
    Ajoute au prompt système le contexte propre au chat.

    Ce contexte contient les actualités récupérées lors de la création
    du chat, puis enregistrées en base de données.
    """
    # `deps` reçoit la valeur transmise avec `agent.run_sync(..., deps=...)`.
    # La chaîne vide permet de ne rien ajouter lorsqu'aucun contexte n'existe.
    return ctx.deps or ""


@agent.tool_plain
def search_news(
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """
    Recherche des articles récents sur un sujet.

    Args:
        query: Sujet ou expression à rechercher.
        max_results: Nombre maximal d'articles à retourner.

    Returns:
        Une liste simplifiée d'articles trouvés.
    """
    return fetch_exploration_topic(
        query=query,
        max_results=max_results,
    )


@agent.tool_plain
def current_date() -> str:
    """Retourne la date du jour au format jour/mois/année."""
    return date.today().strftime("%d/%m/%Y")