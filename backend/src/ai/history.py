def build_history(messages):
    """
    Convertit ton JSON chat -> format PydanticAI
    (version simple et compatible)
    """

    history = []

    for msg in messages:

        role = msg["role"]
        content = msg["content"]

        # On reconstruit un format texte simple
        history.append(f"{role}: {content}")

    return "\n".join(history)