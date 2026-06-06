from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from src.database import engine, get_session
from src.models import Chat
from src.auth.dependencies import get_current_user_id
from src.ai.agent import agent
from src.ai.history import build_history

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
#     with Session(engine) as session:
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
#     with Session(engine) as session:

        # 1. récupérer chat
        chat = session.get(Chat, chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat introuvable")

        # 2. sécurité
        if chat.user_id != user_id:
            raise HTTPException(status_code=403, detail="Accès interdit")

        # 3. ajouter message utilisateur
        user_message = {
            "role": "user",
            "content": message.content
        }
        chat.messages = chat.messages + [user_message]
     #    chat.messages.append(user_message)

        # 4. construire historique (sans le dernier message)
        print("\n===== MESSAGES BRUTS =====")
        for m in chat.messages:
            print(m)
            
        history_text = build_history(chat.messages)
        print("HISTORIQUE ENVOYÉ AU LLM :")
        print(history_text)
        

        # 5. prompt complet envoyé au modèle
        full_prompt = f"""
             Historique de la conversation :
                {history_text}

             Nouveau message utilisateur :
                {message.content}
        """
        
        print("\n===== PROMPT FINAL =====")
        print(full_prompt)
        
        # 6. appel LLM
        result = agent.run_sync(full_prompt)

     #    result = agent.run_sync(
     #         message.content
     #    )

        assistant_response = result.output

        # 7. ajout réponse assistant dans le chat
        print("\n===== RÉPONSE LLM =====")
        print(assistant_response)
        assistant_message = {
            "role": "assistant",
            "content": assistant_response
        }

     #    chat.messages.append(assistant_message)
        chat.messages = chat.messages + [assistant_message]
        print("\n===== CHAT FINAL STOCKÉ =====")
        for m in chat.messages:
            print(m)
            
        # 8. sauvegarde
        session.add(chat)
        session.commit()
        session.refresh(chat)

        return {
            "response": assistant_response,
            "chat": chat.messages
        }