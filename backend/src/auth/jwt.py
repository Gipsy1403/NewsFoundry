# Import des classes permettant de gérer les dates et les durées
from datetime import datetime, timedelta, timezone

# Import de la bibliothèque permettant de créer des JWT
from jose import jwt
from dotenv import load_dotenv
import os

# Charge les variables du fichier .env
load_dotenv()


print("SECRET_KEY =", os.getenv("SECRET_KEY"))
print("ALGORITHM =", os.getenv("ALGORITHM"))
print(
    "ACCESS_TOKEN_EXPIRE_MINUTES =",
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)
# Récupération des variables d'environnement
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# os.getenv retourne une chaîne de caractères,
# on convertit donc la durée en entier
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)


def create_access_token(data: dict):
    """
    Crée un token JWT à partir des données reçues.
    
    Paramètre :
        data (dict) : informations à stocker dans le token
                      (par exemple l'identifiant ou l'email de l'utilisateur)

    Retour :
        str : token JWT généré
    """

    # Création d'une copie du dictionnaire reçu
    # Cela évite de modifier les données d'origine
    to_encode = data.copy()

    # Calcul de la date d'expiration :
    # - datetime.now(timezone.utc) récupère la date actuelle en UTC
    # - timedelta ajoute 60 minutes
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Ajout de la clé "exp" dans le payload
    # Cette clé est reconnue automatiquement par les JWT
    # pour vérifier si le token a expiré
    to_encode.update({"exp": expire})

    # Création du token JWT
    # jwt.encode() :
    #   - prend les données à stocker
    #   - les signe avec la clé secrète
    #   - utilise l'algorithme HS256
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Retour du token généré
    return encoded_jwt