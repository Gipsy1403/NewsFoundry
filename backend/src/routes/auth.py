from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from src.database import engine
from src.models import User
from src.auth.jwt import create_access_token
from src.auth.dependencies import get_current_user_id
from passlib.context import CryptContext

router = APIRouter()

# Gestion des mots de passe hashés
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: str
    password: str

@router.get("/me")
def me(
    user_id: int = Depends(get_current_user_id)
):
    return {
        "user_id": user_id
    }

@router.post("/login")
def login(data: LoginRequest):
    """
    Authentifie un utilisateur et retourne un JWT
    """

    with Session(engine) as session:

        # 1. Chercher utilisateur en base
        user = session.exec(
            select(User).where(User.email == data.email)
        ).first()

        # 2. Vérification unique (sécurité)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Identifiants invalides"
            )

        # 4. Créer token JWT
        token = create_access_token(
            data={"user_id": user.id, "email": user.email}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }