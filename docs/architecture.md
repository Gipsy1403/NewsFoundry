# Architecture du projet

## Structure générale

- `backend/` : code du serveur REST et de la logique métier.
- `frontend/` : application utilisateur Next.js / React.
- `docs/` : documentation technique du projet.
- `README.md` : résumé fonctionnel et technologique global.
- `Makefile` : raccourcis de commandes utiles, notamment pour les tests backend.

## Backend

- `backend/src/main.py` : point d’entrée FastAPI.
- `backend/src/routes/` : routes API exposées par le backend.
- `backend/src/auth/` : gestion de l’authentification, des JWT et des dépendances.
- `backend/src/ai/` : logique des agents IA, récupération de news et génération de revues de presse.
- `backend/src/database.py` : configuration de la base de données et session SQLModel.
- `backend/src/models.py` : définitions des modèles de données SQLModel.
- `backend/src/utils/` : fonctions utilitaires partagées.
- `backend/tests/` : tests unitaires et d’intégration du backend.
- `backend/README.md` : instructions spécifiques d’installation et d’exécution du backend.

## Frontend

- `frontend/src/app/` : architecture Next.js avec layout global et pages.
- `frontend/src/app/(pages)/layout.jsx` : layout de l’application.
- `frontend/src/app/(pages)/PageShell.jsx` : shell client chargé de l’état du drawer mobile.
- `frontend/src/app/components/` : composants réutilisables de l’interface.
- `frontend/src/app/components/Headers/` : en-têtes et navigation.
- `frontend/src/app/components/Footer.jsx` : composant de pied de page.
- `frontend/src/app/components/Modal.jsx` : composant modal générique.
- `frontend/src/app/components/SideBar.jsx` : composant de barre latérale.
- `frontend/src/app/(pages)/chat/`, `home/`, `pressreview/` : pages principales de l’application.
- `frontend/src/context/` : contexte React pour partager l’état chat et revue de presse.
- `frontend/src/lib/api/` : services d’appel aux API backend.
- `frontend/src/styles/` : styles CSS modules.

## Rôles des principaux dossiers

- `backend/` : gère l’API, la base de données, l’authentification et l’intelligence artificielle.
- `frontend/` : gère l’interface utilisateur, les interactions, la navigation et les appels au backend.
- `docs/` : réunit la documentation technique du projet pour les nouveaux contributeurs.
