from src.auth.jwt import ALGORITHM, SECRET_KEY, create_access_token
from jose import jwt


def test_login_success_returns_jwt(client):
    """
    Vérifie qu'un utilisateur avec des identifiants valides
    peut se connecter et reçoit un JWT.
    """
    response = client.post(
        "/login",
        json={
            "email": "test@test.com",
            "password": "test",
        },
    )

    # La connexion doit réussir.
    assert response.status_code == 200

    data = response.json()

    # Le token JWT doit être présent dans la réponse.
    assert "access_token" in data

    # Le type de token attendu est "bearer".
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials_returns_401(client):
    """
    Vérifie qu'une tentative de connexion avec de mauvais
    identifiants est refusée.
    """
    response = client.post(
        "/login",
        json={
            "email": "wrong@test.com",
            "password": "wrong",
        },
    )

    # La requête doit être rejetée.
    assert response.status_code == 401

    # Le message d'erreur attendu est renvoyé.
    assert response.json()["detail"] == "Identifiants invalides"


def test_create_access_token_contains_user_id():
    """
    Vérifie que le JWT généré contient bien l'identifiant
    de l'utilisateur dans son payload.
    """
    # Création d'un token contenant l'id utilisateur.
    token = create_access_token({"user_id": 123})

    # Décodage du token avec la clé secrète de l'application.
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    # Vérifie que le payload contient le bon identifiant.
    assert payload["user_id"] == 123