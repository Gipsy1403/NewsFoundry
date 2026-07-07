from types import SimpleNamespace

from src.routes.pressReviews import create_press_review, PressReviewRequest
from src.models import Chat


def test_create_press_review_success(session, monkeypatch):
    # Prépare un chat en base
    chat = Chat(user_id=1, messages=[{"role": "user", "content": "Bonjour"}], context="ctx")
    session.add(chat)
    session.commit()
    session.refresh(chat)

    # Simule l'agent IA
    class Out:
        def __init__(self):
            self.global_summary = "GLOB"
            self.article_summaries = [SimpleNamespace(title="T1", summary="S1")]
            self.perspectives = "PERS"

    def fake_run_sync(prompt, message_history=None):
        return SimpleNamespace(output=Out())

    import src.ai.pressReviewAgent as pra
    monkeypatch.setattr(pra.press_review_agent, "run_sync", fake_run_sync)

    data = PressReviewRequest(subject="économie")

    review = create_press_review(chat.id, data, user_id=chat.user_id, session=session)

    assert review.subject == "économie"
    assert "REVUE DE PRESSE" in review.title
    assert "Synthèse" in review.markdown_content or "Synthèse" in review.title
