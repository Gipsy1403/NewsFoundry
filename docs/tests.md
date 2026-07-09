# Lancement des tests

## Commande principale

Depuis la racine du projet :

```bash
cd frontend
npm run test-backend
```

Ou directement depuis le backend :

```bash
cd backend
.venv\Scripts\activate
pytest -q
```

Pour obtenir davantage de détails sur les tests exécutés :

```bash
pytest -v
```

---

# Ce que couvrent les tests

Les tests vérifient notamment :

- l'authentification utilisateur (`/login`) ;
- la création et la validation des tokens JWT ;
- les dépendances FastAPI (authentification et utilisateur courant) ;
- les routes des chats :
  - création d'un chat ;
  - consultation d'un chat ;
  - envoi de messages ;
  - historique des conversations ;
  - protection des accès entre utilisateurs ;
- la création des revues de presse et les contrôles d'autorisation ;
- les fonctions de récupération et de formatage des actualités World News ;
- la génération des résumés d'actualités ;
- la conversion de l'historique des conversations vers le format attendu par PydanticAI.

---

# Environnement de test

Les tests utilisent un environnement isolé :

- une base SQLite en mémoire ;
- un utilisateur de test créé automatiquement ;
- les appels au LLM sont simulés (mockés) ;
- les appels à l'API World News sont simulés (mockés) ;
- aucune connexion Internet n'est nécessaire ;
- la base de données est recréée avant chaque test afin de garantir leur indépendance.

---

# Organisation des tests

Les tests sont regroupés dans :

```text
backend/tests/
├── conftest.py
├── test_auth.py
├── test_chats.py
├── test_dependencies.py
├── test_fetch_world_news.py
├── test_history.py
├── test_news.py
└── test_press_reviews.py
```

---

# Notes

- Le script `test-backend` du frontend exécute directement les tests du backend en utilisant l'environnement virtuel Python situé dans `backend/.venv`.
- Avant d'exécuter les tests, vérifier que les dépendances sont installées :

```bash
cd backend
uv sync
```

- Les tests sont entièrement isolés : ils n'utilisent ni la base de données de développement, ni les services IA réels, ni l'API World News.