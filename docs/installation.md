# Installation et exécution

## Prérequis

- Docker
- Python 3.13
- `uv`
- Node.js 22.19

## Installation

1. Cloner le repository.
2. Copier `backend/.env.example` vers `backend/.env` et adapter les variables si nécessaire.
3. Installer les dépendances backend depuis `backend/` :

```bash
cd backend
uv sync
```

4. Installer les dépendances frontend depuis `frontend/` :

```bash
cd frontend
npm install
```

## Lancer le backend

1. Démarrer PostgreSQL avec Docker :

```bash
docker run \
  --name newsfoundry_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=newsfoundry \
  -p 5432:5432 \
  postgres:17
```

2. Démarrer le backend :

```bash
cd backend
uv run --env-file .env -m src.main
```

## Lancer le frontend

Depuis `frontend/` :

```bash
npm run dev
```

## Commandes utiles

- `npm run build` : build du frontend.
- `npm start` : démarrer le frontend en production.
- `npm run lint` : lancer ESLint sur le frontend.
- `npm run test-backend` : exécuter les tests backend depuis le frontend.
