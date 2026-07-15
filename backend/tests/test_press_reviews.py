from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from src.models import Chat
from src.routes.pressReviews import PressReviewRequest, create_press_review


def create_chat_in_db(session, user_id=1):
    """
    Crée un chat de test en base de données
    et retourne l'objet créé.
    """
    chat = Chat(
        user_id=user_id,
        messages=[
            {
                "role": "user",
                "content": "Parle-moi d'économie.",
            }
        ],
        context="ctx",
    )

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat


def test_create_press_review_success(session, monkeypatch):
    """
    Vérifie qu'une revue de presse est correctement générée
    et enregistrée lorsque toutes les conditions sont réunies.
    """
    chat = create_chat_in_db(session, user_id=1)

    class FakePressReviewOutput:
        """Réponse simulée du LLM."""

        global_summary = "Synthèse globale"
        article_summaries = [
            SimpleNamespace(
                title="Article 1",
                summary="Résumé 1",
            )
        ]
        perspectives = "Perspectives"

    def fake_run_sync(*args, **kwargs):
        """Remplace l'appel réel au LLM."""
        return SimpleNamespace(output=FakePressReviewOutput())

    import src.routes.pressReviews as press_reviews_route

    # Remplace le LLM par une réponse simulée.
    monkeypatch.setattr(
        press_reviews_route.press_review_agent,
        "run_sync",
        fake_run_sync,
    )

    review = create_press_review(
        chat.id,
        PressReviewRequest(subject="économie"),
        user_id=1,
        session=session,
    )

    # Vérifie que les informations principales sont bien générées.
    assert review.subject == "économie"
    assert "REVUE DE PRESSE ÉCONOMIE" in review.title
    assert "Synthèse globale" in review.markdown_content
    assert "Article 1" in review.markdown_content
    assert "Perspectives" in review.markdown_content


def test_create_press_review_unknown_chat_returns_404(session):
    """
    Vérifie qu'une erreur 404 est renvoyée
    lorsque le chat demandé n'existe pas.
    """
    with pytest.raises(HTTPException) as exc:
        create_press_review(
            999,
            PressReviewRequest(subject="économie"),
            user_id=1,
            session=session,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Chat introuvable"


def test_create_press_review_for_another_user_returns_403(session):
    """
    Vérifie qu'un utilisateur ne peut pas créer
    une revue de presse à partir du chat d'un autre utilisateur.
    """
    chat = create_chat_in_db(session, user_id=1)

    with pytest.raises(HTTPException) as exc:
        create_press_review(
            chat.id,
            PressReviewRequest(subject="économie"),
            user_id=2,
            session=session,
        )

    assert exc.value.status_code == 403
    assert exc.value.detail == "Accès interdit"
