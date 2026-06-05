from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import engine
from src.models import Chat
from src.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/chats")
def create_chat(
#   Vérifie que l'utilisateur est authentifié avant de créer un chat
    user_id: int = Depends(get_current_user_id)
):
    with Session(engine) as session:
      # Création du chat si l'utilisateur est authentifié
        chat = Chat(
            user_id=user_id,
            messages=[]
        )

        session.add(chat)
        session.commit()
     #    Recharge le chat pour avoir la bonne valeur de l'id généré par la base de données
        session.refresh(chat)

        return {
            "chat_id": chat.id
        }