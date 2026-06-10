from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from src.database import engine, get_session
from src.models import Chat
from src.auth.dependencies import get_current_user_id
from src.ai.agent import agent
from src.ai.history import build_history
from src.ai.news import (build_news_system_prompt, build_news_context)
from datetime import datetime

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

@router.post("/chats")
def create_chat(
#   Vérifie que l'utilisateur est authentifié avant de créer un chat
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):

    # 1. construire system prompt + news du jour
    system_prompt = f"""
      {build_news_system_prompt()}

      [ACTUALITÉS DU JOUR]

      {build_news_context()}
     """
      # Création du chat si l'utilisateur est authentifié
    chat = Chat(
            user_id=user_id,
            messages=[],
            system_prompt=system_prompt,
        )

    session.add(chat)
    session.commit()
     #    Recharge le chat pour avoir la bonne valeur de l'id généré par la base de données
    session.refresh(chat)

    return {
        "id": chat.id,
        "user_id": chat.user_id,
        "messages": chat.messages,
        "system_prompt": chat.system_prompt,
        "created_at": chat.created_at.isoformat()  # important pour React
        }
    
class MessageRequest(BaseModel):
    content: str

# Envoi un message dans un chat spécifique de l'utilisateur connecté
@router.post("/chats/{chat_id}/messages")
def send_message(
    chat_id: int,
    message: MessageRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
        # 1. récupérer chat
        chat = session.get(Chat, chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat introuvable")

        # 2. sécurité
        if chat.user_id != user_id:
            raise HTTPException(status_code=403, detail="Accès interdit")

        # 3. construire historique (sans le dernier message)
        history_text = build_history(chat.messages)
        
        # 4. ajouter message utilisateur
        user_message = {
            "role": "user",
            "content": message.content
        }
        chat.messages = chat.messages + [user_message]

        # ETAPE 5 : on préfixe le prompt avec le system_prompt sauvegardé en BDD
        # ✅ C'est la façon fiable d'injecter le contexte dans pydantic-ai
        # car run_sync() ne supporte pas de paramètre system_prompt à la volée
        # Les anciens chats sans system_prompt fonctionnent normalement (fallback sur le prompt de l'agent)
        
        system_prompt = (chat.system_prompt or build_news_system_prompt())
        
        full_prompt = f"""
			{system_prompt}

			[Historique]
			{history_text}

			[Nouveau message utilisateur]
			{message.content}
	    """

        # 6. appel LLM
        result = agent.run_sync(full_prompt)

     #    assistant_response = result.output

        # 7. Sauvegarde de la réponse de l'assistant dans l'historique du chat
        assistant_message = {
            "role": "assistant",
            "content": result.output
        }

     #    chat.messages.append(assistant_message)
        chat.messages = chat.messages + [assistant_message]
            
        # 8. sauvegarde
        session.add(chat)
        session.commit()
        session.refresh(chat)

        return {
            "response": result.output,
            "chat": chat.messages
        }