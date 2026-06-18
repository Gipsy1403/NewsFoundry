from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.types import JSON
from datetime import datetime, timezone


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field()

class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # lien avec l'utilisateur propriétaire
    user_id: int = Field(index=True)

    # historique complet du chat
    messages: List[Dict[str, Any]] = Field(
        sa_column=Column(JSON, nullable=False),
        default_factory=list
    )

    # Stockage du system prompt utilisé à la création du chat
    # Optional[str] car les anciens chats n'en auront pas (rétrocompatibilité)
    context: Optional[str] = Field(default=None)

#     Date de création du chat
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class PressReview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # discussion à l'origine de la revue de presse
    chat_id: int = Field(index=True)
    # sujet choisi par l'utilisateur
    subject: str
    # titre généré par l'agent
    title: str
#     # synthèse générale du sujet
#     global_summary: str
#     # résumés par article : liste de {"article_title": ..., "summary": ...}
#     article_summaries: List[Dict[str, Any]] = Field(
#         sa_column=Column(JSON, nullable=False),
#         default_factory=list
#     )
    markdown_content:str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )