from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.types import JSON


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
    system_prompt: Optional[str] = Field(default=None)