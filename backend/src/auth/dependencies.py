from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt # Bibliothèque python qui permet de créer, signer, et décoder des jetons JWT (JSON Web Tokens)
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Vérifie le JWT et retourne l'identifiant de l'utilisateur authentifié.
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["user_id"]

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )