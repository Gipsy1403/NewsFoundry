from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from pydantic_ai.exceptions import ModelHTTPError

from src.database import get_session
from src.models import Chat, PressReview
from src.auth.dependencies import get_current_user_id
from src.ai.history import build_history
from src.ai.pressReviewAgent import press_review_agent

router = APIRouter()


class PressReviewRequest(BaseModel):
    subject: str


# Génère une revue de presse pour un chat donné, sur un sujet précis (bouton "Générer la revue de presse")
@router.post("/chats/{chat_id}/press-reviews")
def create_press_review(
    chat_id: int,
    data: PressReviewRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    try:
        print("ETAPE 1")

        chat = session.get(Chat, chat_id)

        if not chat:
            raise HTTPException(status_code=404, detail="Chat introuvable")

        if chat.user_id != user_id:
            raise HTTPException(status_code=403, detail="Accès interdit")

        history = build_history(chat.messages)

        # 🧠 appel IA avec gestion d'erreur spécifique
        try:
            result = press_review_agent.run_sync(
                f"Sujet de la revue de presse : {data.subject}",
                message_history=history,
            )

        except ModelHTTPError:
            raise HTTPException(
                status_code=503,
                detail="Le service IA est temporairement indisponible."
            )

        output = result.output

        press_review = PressReview(
            chat_id=chat.id,
            subject=data.subject,
            title=output.title,
            markdown_content=output.markdown_content,
        )

        session.add(press_review)
        session.commit()
        session.refresh(press_review)

        return press_review

    except Exception as e:
        print("🔥 ERREUR =", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue"
        )

# @router.post("/chats/{chat_id}/press-reviews")
# def create_press_review(
#     chat_id: int,
#     data: PressReviewRequest,
#     user_id: int = Depends(get_current_user_id),
#     session: Session = Depends(get_session),
# ):
#     try:
#         print("ETAPE 1")
#         chat = session.get(Chat, chat_id)

#         if not chat:
#             raise HTTPException(status_code=404, detail="Chat introuvable")

#         if chat.user_id != user_id:
#             raise HTTPException(status_code=403, detail="Accès interdit")


#         history = build_history(chat.messages)

#         result = press_review_agent.run_sync(
#             f"Sujet de la revue de presse : {data.subject}",
#             message_history=history,
#         )

#         output = result.output

#         press_review = PressReview(
#             chat_id=chat.id,
#             subject=data.subject,
#             title=output.title,
#             markdown_content=output.markdown_content,
#         )

#         session.add(press_review)
#         session.commit()
#         session.refresh(press_review)

#         return press_review

#     except Exception as e:
#         print("🔥 ERREUR =", repr(e))
#         raise HTTPException(
#             status_code=500,
#             detail="Une erreur interne est survenue"
# 	   )


# Liste toutes les revues de presse de l'utilisateur connecté (toutes discussions confondues) (Page/review)
@router.get("/press-reviews")
def list_press_reviews(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    chat_ids = session.exec(
        select(Chat.id).where(Chat.user_id == user_id)
    ).all()

    if not chat_ids:
        return []

    reviews = session.exec(
        select(PressReview)
        .where(PressReview.chat_id.in_(chat_ids))
        .order_by(PressReview.created_at.desc())
    ).all()

    return reviews


# Détail d'une revue de presse spécifique
@router.get("/press-reviews/{review_id}")
def get_press_review(
    review_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    review = session.get(PressReview, review_id)

    if not review:
        raise HTTPException(status_code=404, detail="Revue introuvable")

    chat = session.get(Chat, review.chat_id)

    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    return review