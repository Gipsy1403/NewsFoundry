# Choix techniques

## Frontend

- **Next.js 16.2.6** avec App Router pour organiser les pages et le routage.
- **React 19.2.4** pour construire les interfaces.
- **CSS Modules** pour isoler les styles au niveau des composants.
- **FontAwesome** pour les icônes.
- **Radix UI** pour des composants accessibles, comme les avatars et les dialogues.
- **react-hot-toast** pour les notifications utilisateur.
- **react-markdown** pour l’affichage de contenu texte formaté.

### Justification

- Next.js est bien adapté à un projet web moderne avec rendu côté client et génération statique.
- CSS Modules évite les conflits de classes et facilite la maintenance des styles.
- Radix UI fournit des composants accessibles et modulaires.

## Backend

- **Python 3.13** pour exploiter l’écosystème IA et data.
- **FastAPI** pour une API performante, simple et bien documentée.
- **SQLModel** pour gérer les modèles de données et la base SQL de façon déclarative.
- **PostgreSQL** comme base de données relationnelle.
- **JWT** pour l’authentification et la sécurisation des routes.
- **python-jose** et **passlib[bcrypt]** pour les tokens et le hachage des mots de passe.
- **pydantic-ai** pour l’interface avec les services IA.

### Justification

- Python et FastAPI permettent de prototyper rapidement les endpoints et d’assurer de bonnes performances.
- SQLModel est cohérent avec FastAPI et simplifie la sérialisation des données.
- Les JWT sécurisent les échanges entre frontend et backend tout en restant légers.
- Le choix de PostgreSQL correspond à une base fiable et compatible avec SQLAlchemy/SQLModel.

## Tests

- Le backend utilise **pytest** pour les tests.
- Les tests sont exécutables depuis le dossier `backend/`.
- Le frontend contient un script `test-backend` qui déclenche les tests backend depuis `frontend/package.json`.

## Déploiement en production

L'application est prévue pour être déployée avec trois services principaux.
|-----------------------------|--------------|----------------------------------------------------------------|
| Élément				 	| Plateforme 	| Rôle 												|
|-----------------------------|--------------|----------------------------------------------------------------|
| Backend FastAPI 			| Railway		| Héberger l'API REST et la logique IA. 					|
| Base de données PostgreSQL 	| Railway 	| Stocker les utilisateurs, chats, messages et revues de presse. |
| Frontend Next.js 			| Vercel 		| Héberger l'interface utilisateur. 						|
|-----------------------------|--------------|----------------------------------------------------------------|

### URL de production

```text
URL frontend Vercel : https://news-foundry-delta.vercel.app
```


### Variables d'environnement backend

Le backend nécessite notamment :

```text
DATABASE_URL=<url_postgresql_railway>
SECRET_KEY=<clé_secrète_jwt>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
MISTRAL_API_KEY=<clé_api_mistral>
WORLD_NEWS_API_KEY=<clé_api_worldnewsapi>
```

Ces variables doivent être configurées dans Railway.

### Variables d'environnement frontend

Le frontend doit connaître l'URL du backend déployé.

```text
NEXT_PUBLIC_API_URL=https://newsfoundry-production-55cc.up.railway.app
```

Cette variable doit être configurée dans Vercel.

## Déploiement automatique

Le projet utilise un déploiement automatique à partir de la branche `main`.

### Frontend sur Vercel

Vercel est relié au repository GitHub.
À chaque nouveau commit sur la branche `main` :

1. Vercel détecte le changement ;
2. Vercel lance le build du frontend ;
3. Vercel publie automatiquement la nouvelle version.

### Backend sur Railway

Railway est relié au repository GitHub.
À chaque nouveau commit sur la branche `main` :

1. Railway détecte le changement ;
2. Railway reconstruit le service backend ;
3. Railway redéploie l'API automatiquement.

### Base de données sur Railway

La base PostgreSQL est hébergée dans Railway.
Le backend utilise la variable `DATABASE_URL` pour se connecter à cette base.

## Intégration continue avec GitHub Actions

Les tests backend sont automatisés avec GitHub Actions.

Le fichier à créer est :

```text
.github/workflows/backend-tests.yml
```

Cette action lance les tests automatiquement :

- à chaque push sur `main` ;
- à chaque pull request vers `main`.

Elle vérifie donc que les tests backend passent avant validation du code.

