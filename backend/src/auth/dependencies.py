# from fastapi import Header, HTTPException

# from jose import jwt
# import os

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")


# def get_current_user_id(
# #     FastAPI lir automatiquement le Header "Authorization" et le passera à cette fonction
#     authorization: str = Header(...)
# ):
#     """
#     Extrait le user_id contenu dans le JWT.
#     """

#     try:
#      #  Retrait du terme Bearer pour n'avoir que le token lui-même
#         token = authorization.replace(
#             "Bearer ",
#             ""
#         )
#      #  Vérification du token et extraction du payload
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )
#      #  Lors du login, récupération du user_ et du email, mais ici je n'ai besoin que du user_id
#         return payload["user_id"]
    
#     except Exception:
#         raise HTTPException(
#             status_code=401,
#             detail="Token invalide"
#         )

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials  # le JWT brut

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