import os
from src.models import User
from sqlmodel import SQLModel, Session, create_engine, select
from passlib.context import CryptContext

# Récupère l'URL de la base de données depuis les variables d'environnement.
# Si aucune variable d'environnement n'est définie, utilise une base de données SQLite locale.
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///test.db")

engine = create_engine(DATABASE_URL, echo=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    # Ouvre une session de connexion à la base de données.
    # La session sera utilisée par les routes FastAPI
    # pour lire, ajouter, modifier ou supprimer des données.
    # Grâce au mot-clé "with", la session sera fermée
    # automatiquement à la fin de son utilisation.
    with Session(engine) as session:
        # "yield" prête la session à FastAPI.
        # La route qui utilise Depends(get_session)
        # reçoit cette session dans un paramètre.
        yield session
        

def init_db():
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully")

    # Creating a default user
    default_email = "test@test.com"
    default_password = "test"

    with Session(engine) as session:
        statement = select(User).where(User.email == default_email)
        user = session.exec(statement).first()

        if not user:
            session.add(
                User(
                    email=default_email,
                    hashed_password=pwd_context.hash(default_password)
                )
            )
            session.commit()
            


