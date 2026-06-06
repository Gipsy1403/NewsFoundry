import os
from src.models import User
from sqlmodel import SQLModel, Session, create_engine, select
# import bcrypt
from passlib.context import CryptContext

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///test.db")
print(os.getenv("DATABASE_URL"))
engine = create_engine(DATABASE_URL, echo=True)
print("DATABASE_URL =", engine.url)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
                    # hashed_password=bcrypt.hashpw(
                    #     default_password.encode("utf-8"), bcrypt.gensalt()
                    # ),
                    hashed_password=pwd_context.hash(default_password)
                )
            )
            session.commit()
            

def get_session():
    with Session(engine) as session:
        yield session
