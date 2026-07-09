import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.dependencies import get_current_user_id
from src.auth.jwt import create_access_token


def test_get_current_user_id_from_valid_token():
    """
    Vérifie qu'un JWT valide permet de récupérer
    l'identifiant de l'utilisateur.
    """
    # Génère un token contenant l'id utilisateur.
    token = create_access_token({"user_id": 7})

    # Simule l'en-tête Authorization envoyé par le client.
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    # L'id contenu dans le token doit être correctement extrait.
    assert get_current_user_id(credentials) == 7


def test_get_current_user_id_with_invalid_token_raises_401():
    """
    Vérifie qu'un JWT invalide provoque une erreur HTTP 401.
    """
    # Simule un token invalide.
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="bad-token",
    )

    # La dépendance doit lever une exception HTTP.
    with pytest.raises(HTTPException) as exc:
        get_current_user_id(credentials)

    # Le code de retour attendu est 401 (Non autorisé).
    assert exc.value.status_code == 401