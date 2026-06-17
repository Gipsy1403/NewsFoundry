# def build_history(messages):
#     """
#     Convertit JSON chat -> format PydanticAI
#     """

#     history = []

#     for msg in messages:

#         role = msg["role"]
#         content = msg["content"]

#         # On reconstruit un format texte simple
#         history.append({
#             "role": role,
#           "content": content})

#     return history

from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart


def build_history(messages):
    """
    Convertit l'historique JSON stocké en BDD
    (liste de {"role": "user"|"assistant", "content": str})
    en une liste de ModelMessage utilisable comme message_history
    par PydanticAI.
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