# Lancement des tests

## Commande principale

Depuis le dossier racine du projet :

```bash
cd frontend
npm run test-backend
```

ou directement depuis le backend :

```bash
cd backend
.venv\Scripts\python.exe -m pytest -q
```

## Ce que testent les tests

- les routes FastAPI (authentification, chats, revues de presse)
- les dépendances d’authentification JWT
- les interactions avec la base de données en mémoire
- les composants IA et les agents qui analysent ou génèrent du contenu
- les services backend exposés au frontend

## Notes

- Le script `test-backend` du frontend lance directement les tests backend en référençant l’environnement Python virtuel du backend.
- Les tests sont situés dans `backend/tests/`.
