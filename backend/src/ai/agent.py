from pydantic_ai import Agent
import os
print("import ok")
# Exemple avec OpenAI (ou autre provider selon ton choix)
# Ici on suppose OPENAI_API_KEY dans .env

agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt=(
        "Tu es l'assistant IA de NewsFoundry. "
        "Tu aides l'utilisateur à comprendre et analyser des informations. "
        "Tu réponds de manière claire, structurée et utile."
    )
)