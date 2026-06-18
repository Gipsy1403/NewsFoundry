from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from typing import List
import os

print(
    "KEY FOUND:",
    bool(os.getenv("MISTRAL_API_KEY"))
)

model = MistralModel("mistral-small")


class ArticleSummary(BaseModel):
    title: str = Field(
        description="Titre de l'article résumé"
    )
    summary: str = Field(
        description="Résumé de l'article en lien avec le sujet demandé"
    )


class PressReviewOutput(BaseModel):
    title: str = Field(
        description="Titre global de la revue de presse"
    )
#     markdown_content:str
    global_summary: str = Field(
        description="Synthèse globale de la revue de presse"
    )

    article_summaries: List[ArticleSummary] = Field(
        description="Synthèse des articles évoqués"
    )

    perspectives: str = Field(
        description="Analyse des tendances et perspectives"
    )


press_review_agent = Agent(
    model,
    output_type=PressReviewOutput,
    system_prompt="""
Tu es un journaliste spécialisé dans les revues de presse.

Tu dois analyser une conversation complète.

OBJECTIF :
- synthétiser les sujets abordés dans la discussion
- regrouper les thèmes similaires
- produire une revue de presse structurée

CONTRAINTES :
- ne pas inventer d'informations
- utiliser uniquement le contexte fourni dans l'historique
- rester factuel et neutre

"""
)

