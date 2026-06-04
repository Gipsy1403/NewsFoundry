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

        # 2. Vérifier existence
        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur introuvable")

        # 3. Vérifier mot de passe
        print("HASH DB =", user.hashed_password)
        print("TYPE =", type(user.hashed_password))
        
        if not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

        # 4. Créer token JWT
        token = create_access_token(
            data={"user_id": user.id, "email": user.email}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }