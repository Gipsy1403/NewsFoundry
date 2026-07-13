## Erreurs retournées par l'API

Le backend utilise `HTTPException` de FastAPI pour retourner des erreurs claires au frontend.
Ces erreurs permettent aussi d'afficher un message compréhensible à l'utilisateur dans l'interface.


### Authentification

**POST `/login`**

- **Code HTTP :** `401`
- **Message :** `Identifiants invalides`
- **Cause :** email ou mot de passe incorrect.

**Routes protégées**

- **Code HTTP :** `401`
- **Message :** `Erreur d'authentification`
- **Cause :** token JWT absent, invalide ou expiré.

---

### Gestion des chats

**GET `/chats/{chat_id}`**

- **404** — `Chat introuvable`
- Le chat demandé n'existe pas.

- **403** — `Accès interdit`
- L'utilisateur tente d'accéder au chat d'un autre utilisateur.

**POST `/chats/{chat_id}/messages`**

- **404** — `Chat introuvable`
- Impossible d'ajouter un message dans un chat inexistant.

- **403** — `Accès interdit`
- La logique d'autorisation empêche toute modification d'un chat appartenant à un autre utilisateur.


**POST `/chats`**

- **500** — `Erreur lors de la création du chat`
- Cause : erreur lors de la récupération des actualités ou problème lors de la sauvegarde en base de données.

---

### Revues de presse

**POST `/chats/{chat_id}/press-reviews`**

- **404** — `Chat introuvable`
- Le chat n'existe pas.

- **403** — `Accès interdit`
- Le chat appartient à un autre utilisateur.

- **503** — `Service IA indisponible`
- Le modèle LLM ou un service externe n'a pas répondu correctement.

**GET `/press-reviews/{review_id}`**

- **404** — `Revue introuvable`
- La revue demandée n'existe pas.

- **403** — `Accès interdit`
- La revue appartient à un autre utilisateur.

---

### Erreurs serveur

**GET `/chats`**

- **500** — `Erreur lors de la récupération des chats`
- Une erreur interne est survenue lors de l'accès à la base de données.


### Gestion côté frontend

Les appels API du frontend passent par une couche de service dédiée.
Lorsqu'une erreur se produit :

- l'erreur est capturée côté frontend ;
- un message est affiché à l'utilisateur ;
- l'interface évite de rester bloquée ;
- les loaders permettent d'indiquer que la demande est en cours.

Cette logique améliore l'expérience utilisateur, car l'utilisateur comprend ce qui se passe en cas de problème.