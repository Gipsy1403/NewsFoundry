from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart


def convert_history_for_pydantic(messages):
    """
    Convertit l'historique JSON stocké en BDD
    (liste de {"role": "user"|"assistant", "content": str})
    en une liste utilisable par PydanticAI.
    """

    history = []

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            history.append(
                ModelRequest(parts=[UserPromptPart(content=content)])
            )
        elif role == "assistant":
            history.append(
                ModelResponse(parts=[TextPart(content=content)])
            )
            
    return history
