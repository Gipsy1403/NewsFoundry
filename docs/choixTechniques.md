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

## Déploiement

- Le backend est prévu pour être packagé avec un **Dockerfile**.
- Le frontend est conçu pour être déployé principalement sur **Vercel**.
- Le backend peut être déployé sur des plateformes comme **Railway**.
