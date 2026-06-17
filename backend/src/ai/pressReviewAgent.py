from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
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
    markdown_content:str
#     global_summary: str = Field(
#         description="Synthèse générale du sujet"
#     )
#     article_summaries: list[ArticleSummary] = Field(
#         description="Résumés des articles évoqués dans la conversation en lien avec le sujet"
#     )


press_review_agent = Agent(
    model,
    output_type=PressReviewOutput,
    system_prompt="""
Tu es un journaliste spécialisé dans la rédaction de revues de presse.

Tu dois produire UNIQUEMENT un texte au format Markdown.

Structure obligatoire :

# {title}

## Synthèse des principales actualités

### Sujet 1
Résumé clair en 2-3 phrases.

### Sujet 2
Résumé clair en 2-3 phrases.

### Sujet 3
Résumé clair en 2-3 phrases.

## Perspectives

Conclusion générale en 3-4 phrases.

Contraintes :
- Utilise uniquement du Markdown
- Pas de JSON
- Pas de texte hors structure
- Concentre-toi uniquement sur le sujet demandé

"""
)

