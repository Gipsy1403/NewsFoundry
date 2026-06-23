import pytest
from src.routes.auth import login, LoginRequest, pwd_context
from src.models import User


def test_login_success(session):
    # Création d'un utilisateur en base
    user = User(email="u@test.com", hashed_password=pwd_context.hash("secret"))
    session.add(user)
    session.commit()
    session.refresh(user)

    data = LoginRequest(email="u@test.com", password="secret")
    resp = login(data, session=session)
    assert "access_token" in resp
    assert resp["token_type"] == "bearer"


def test_login_invalid_credentials(session):
    data = LoginRequest(email="nope@test.com", password="x")
    with pytest.raises(Exception):
        # l'endpoint lève HTTPException sur identifiants invalides
        login(data, session=session)
