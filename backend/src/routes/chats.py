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

	# Retourne à l'écran (front)
#     return {
#         "id": chat.id,
#         "user_id": chat.user_id,
#         "messages": chat.messages,
#         "system_prompt": chat.system_prompt,
#         "created_at": chat.created_at.isoformat()  # important pour React
#         }
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

        # 3. construit l'historique 
        history_text = build_history(chat.messages)
        
        # 4. le message utilisateur est ajouté à l'historique
        user_message = {
            "role": "user",
            "content": message.content
        }
        chat.messages = chat.messages + [user_message]
        
        full_prompt = f"""
{chat.system_prompt}

[HISTORIQUE]
{history_text}

[QUESTION]
{message.content}
"""

        
#      #   5.récupère et filtres les news
#         articles = fetch_top_news()
#      #    filtered_articles = filter_articles(
#      #      articles,
#      #      message.content
#      #  )
#         filtered_articles = articles[:15]
        
# 	#   6.les articles filtrés sont transformés en texte
#         formatted_articles = "\n\n".join([
#     f"Titre: {a['title']}\nRésumé: {a['summary']}"
#     for a in filtered_articles
# ])

#         # 7.Construit le prompt au complet
        
#         system_prompt = (chat.system_prompt or build_news_system_prompt())
        
#         print("=== SYSTEM PROMPT ===")
#         print(chat.system_prompt)
        

#         full_prompt = f"""
#         {system_prompt}

#         [HISTORIQUE]
#         {history_text}

#         [ACTUALITÉS FILTRÉES]
#         {formatted_articles}

#         [QUESTION UTILISATEUR]
#         {message.content}
#         """
        
        
        # 8. Envoi le prompt à l'IA
        result = agent.run_sync(full_prompt)


        # 9. Récupération de la réponse de l'IA
        assistant_message = {
            "role": "assistant",
            "content": result.output
        }
        chat.messages = chat.messages + [assistant_message]
            
        # 10. sauvegarde en base
        session.add(chat)
        session.commit()
        session.refresh(chat)

	# 11.Retour dans le frontend
        return {
            "response": result.output,
            "chat": chat.messages
        }