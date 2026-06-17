from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from src.database import engine, get_session
from src.models import Chat
from src.auth.dependencies import get_current_user_id
from src.ai.agent import agent
from src.ai.history import build_history
from src.ai.news import (build_news_system_prompt, fetch_top_news, filter_articles)
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified


router = APIRouter()

# Récupère tous les chats de l'utilisateur connecté
@router.get("/chats")
def get_chats(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
#     with Session(engine) as session:

        chats = session.exec(
            select(Chat).where(
                Chat.user_id == user_id
            )
        ).all()

        return chats

# Récupère un chat spécifique de l'utilisateur connecté
@router.get("/chats/{chat_id}")
def get_chat(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
#     with Session(engine) as session:

        chat = session.get(Chat, chat_id)

        # Vérifie que le chat existe
        if not chat:
            raise HTTPException(
                status_code=404,
                detail="Chat introuvable"
            )

        # Vérifie que le chat appartient au user connecté
        if chat.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Accès interdit"
            )

        return chat

# Création d'un nouveau chat pour l'utilisateur connecté
@router.post("/chats")
def create_chat(
#   Vérifie que l'utilisateur est authentifié avant de créer un chat
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):

    articles=fetch_top_news()
    # 1. construire system prompt + news du jour
    system_prompt = build_news_system_prompt(articles)
      # Création du chat si l'utilisateur est authentifié
    chat = Chat(
            user_id=user_id,
            messages=[],
            system_prompt=system_prompt,
        )

#   2. sauvegarde du chat en base de données
    session.add(chat)
    session.commit()
     #Recharge le chat pour avoir la bonne valeur de l'id généré par la base de données
    session.refresh(chat)

    return chat

# Structure attendue lorsqu'un utilisteur envoie un message
class MessageRequest(BaseModel):
    content: str

# Gestion de la conversation avec l'IA
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
        flag_modified(chat, "messages")
        
        # 4. historique avant l'ajout du message courant sinon il serait dupliqué.
        history = build_history(chat.messages)
     #    chat.messages = chat.messages + [user_message]
        print("SYSTEM PROMPT DU CHAT", chat.system_prompt)
        # 5. Appel de l'agent

        result=agent.run_sync(
           message.content,
           message_history=history,
           deps=chat.system_prompt
        )
        print("TYPE =", type(result.output))
        # 6. Récupération de la réponse de l'IA
        assistant_message = {
            "role": "assistant",
            "content": result.output
        }
        chat.messages.append(assistant_message)
     #    chat.messages = chat.messages + [assistant_message]
        flag_modified(chat, "messages")
            
        # 7. sauvegarde en base
        session.add(chat)

        
        print("Avant commit :", len(chat.messages))
        session.commit()
        session.refresh(chat)
        print("Après commit :", len(chat.messages))
        
	# 8.Retour dans le frontend
        return {
            "response": result.output,
            "chat": chat.messages
        }


