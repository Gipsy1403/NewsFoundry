from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from src.database import get_session
from src.models import Chat
from src.auth.dependencies import get_current_user_id
from src.ai.conversationalAgent import agent
from src.ai.convertHistoryForPydantic import convert_history_for_pydantic
from src.ai.todayNews import (build_today_news_prompt, fetch_top_news_today_news)
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# -----------------------------------------------------------
# Récupère tous les chats de l'utilisateur connecté
# -----------------------------------------------------------

@router.get("/chats")
def get_chats(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    try:
        chats = session.exec(
            select(Chat).where(Chat.user_id == user_id)
        ).all()

        return chats

    except SQLAlchemyError:
        # Erreur base de données
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des chats"
        )

# -----------------------------------------------------------
# Récupère un chat spécifique de l'utilisateur connecté
# -----------------------------------------------------------

@router.get("/chats/{chat_id}")
def get_chat(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    try:
        chat = session.get(Chat, chat_id)

        # 404 : chat inexistant
        if not chat:
            raise HTTPException(
                status_code=404,
                detail="Chat introuvable"
            )

        # 403 : pas le bon utilisateur
        if chat.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Accès interdit"
            )

        return chat

    except SQLAlchemyError:
        # 500 : erreur base de données
        raise HTTPException(
            status_code=500,
            detail="Erreur serveur lors de la récupération du chat"
        )

# -------------------------------------------------
# Création d'un nouveau chat pour l'utilisateur connecté
# -----------------------------------------------------------

@router.post("/chats")
def create_chat(
#   Vérifie que l'utilisateur est authentifié avant de créer un chat
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    try:
        # Récupération des actualités et construction du contexte
        articles = fetch_top_news_today_news()
        context = build_today_news_prompt(articles)

        # Création du chat si l'utilisateur est authentifié
        chat = Chat(
            user_id=user_id,
            messages=[],
            context=context,
        )

        # Sauvegarde du chat en base de données
        session.add(chat)
        session.commit()
        # Recharge le chat pour avoir la bonne valeur de l'id généré par la base de données
        session.refresh(chat)

        return chat

    except SQLAlchemyError:
        # Annule la transaction et renvoie une erreur 500
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la création du chat"
        )
    except Exception:
        # Erreurs externes (API d'actualités, construction du prompt, etc.)
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la création du chat"
        )



# Structure attendue lorsqu'un utilisteur envoie un message
class MessageRequest(BaseModel):
    content: str

# ------------------------------------------------------
# Gestion de la conversation avec l'IA
# -----------------------------------------------------------

@router.post("/chats/{chat_id}/messages")
def send_message(
    chat_id: int,
    message: MessageRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
        # 1. récupére le chat demandé
        chat = session.get(Chat, chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat introuvable")

        # 2. vérifie la sécurité
        if chat.user_id != user_id:
            raise HTTPException(status_code=403, detail="Accès interdit")
        
        # 3. le message utilisateur est ajouté à l'historique
        user_message = {
            "role": "user",
            "content": message.content
        }
        chat.messages.append(user_message)
        # Indique à SQLAlchemy que la liste des messages a été modifiée pour qu'il puisse gérer correctement la persistance des données lors du prochain commit
        flag_modified(chat, "messages")

        history = convert_history_for_pydantic(chat.messages)

        # 5. Appel de l'agent
        result=agent.run_sync(
           message.content,
           message_history=history,
           deps=chat.context
        )

        # 6. Récupération de la réponse de l'IA
        assistant_message = {
            "role": "assistant",
            "content": result.output

        }
        chat.messages.append(assistant_message)
        flag_modified(chat, "messages")
            
        # 7. sauvegarde en base
        session.add(chat)
        session.commit()
        session.refresh(chat)
        
	# 8.Retour dans le frontend
        return {
            "response": result.output,
            "chat": chat.messages
        }