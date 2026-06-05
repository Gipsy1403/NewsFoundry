from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from src.database import engine
from src.models import User
from src.auth.jwt import create_access_token
from passlib.context import CryptContext

router = APIRouter()

# Gestion des mots de passe hashés
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: str
    password: str


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