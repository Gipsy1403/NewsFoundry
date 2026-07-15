# Justification des choix de prompts

Le projet utilise deux agents IA principaux :

* un agent conversationnel chargé de répondre aux questions liées à l’actualité ;
* un agent spécialisé chargé de générer une revue de presse structurée à partir d’une conversation.

---

## 1. Prompt de l’agent conversationnel

**Fichier :** `backend/src/ai/conversationalAgent.py`

L’agent conversationnel est configuré comme un assistant spécialisé dans l’analyse et la synthèse d’actualités.

### Choix effectués

* Le rôle de l’agent est défini explicitement afin d’éviter des réponses trop générales.
* Les réponses doivent être rédigées en français.
* Le ton attendu est journalistique, neutre, clair et concis.
* L’agent ne doit inventer ni information, ni source, ni titre, ni citation.
* Pour toute question liée à la date actuelle, l’agent doit utiliser l’outil `current_date`.
* L’agent doit utiliser en priorité le contexte d’actualités enregistré avec le chat.
* L’outil `search_news` ne doit être utilisé que lorsqu’une recherche complémentaire est nécessaire, notamment lorsque :

  * l’utilisateur demande explicitement d’approfondir un sujet ;
  * il souhaite obtenir davantage d’informations ;
  * il veut explorer une actualité ;
  * il demande des articles récents ;
  * l’information recherchée n’est pas présente dans le contexte du chat ;
  * il demande une mise à jour plus récente que le contexte disponible.
* Lorsque `search_news` est utilisé, l’agent doit :

  * s’appuyer sur les articles réellement récupérés ;
  * indiquer qu’il s’agit d’une recherche complémentaire ;
  * identifier les points communs entre les articles ;
  * résumer les informations importantes ;
  * citer les titres lorsque cela est pertinent.
* L’agent doit distinguer les informations provenant du contexte initial du chat de celles issues d’une recherche complémentaire.

### Objectifs

* Limiter les hallucinations.
* Améliorer la pertinence et la cohérence des réponses.
* Guider le modèle vers une réponse factuelle.
* Réutiliser les données récupérées depuis World News API comme contexte principal.
* Éviter les appels inutiles à l’outil de recherche.
* Rendre explicite l’origine des informations utilisées dans la réponse.

---

## 2. Prompt de contexte ajouté à chaque chat

**Fichiers concernés :**

* `backend/src/ai/conversationalAgent.py`, fonction `add_chat_context`
* `backend/src/ai/todayNews.py`, fonction `build_today_news_prompt`
* `backend/src/routes/chats.py`

Lorsqu’un nouveau chat est créé, le backend récupère des actualités depuis World News API, construit un contexte textuel, puis l’enregistre dans le champ `context` du chat en base de données.

Lors de chaque nouvel appel à l’agent, ce contexte est transmis avec :

```python
deps=chat.context or ""
```

Pydantic AI rend ensuite cette valeur accessible dans :

```python
ctx.deps
```

La fonction suivante ajoute alors ce contenu au prompt système dynamique de l’agent :

```python
@agent.system_prompt
def add_chat_context(ctx: RunContext[str]) -> str:
    return ctx.deps or ""
```

### Choix effectués

* Fournir au modèle un contexte d’actualités dès la création de la conversation.
* Générer ce contexte une seule fois pour un chat donné.
* Enregistrer ce contexte en base de données afin de pouvoir le réutiliser.
* Réinjecter le même contexte lors de chaque message du chat.
* Utiliser une chaîne vide lorsqu’un ancien chat ne possède pas encore de contexte.
* Demander au modèle d’utiliser ce contexte en priorité.
* Autoriser une recherche externe uniquement lorsqu’elle est nécessaire.
* Demander au modèle de signaler lorsqu’une information n’est pas disponible dans le contexte initial.

### Objectifs

* Éviter que le modèle réponde uniquement à partir de ses connaissances internes.
* Conserver une base d’information commune pendant toute la conversation.
* Améliorer la cohérence entre les réponses successives.
* Réduire le risque d’hallucination.
* Assurer la compatibilité avec les anciens chats dont le champ `context` peut être vide ou égal à `None`.

---

## 3. Récupération et préparation des actualités du jour

**Fichier :** `backend/src/ai/todayNews.py`

La fonction `fetch_top_news_today_news` appelle le endpoint `/top-news` de World News API.

Les paramètres utilisés permettent notamment de demander :

* des sources françaises ;
* des articles en français ;
* des actualités correspondant à la date du jour.

Afin de limiter la quantité de données manipulées, le backend :

* conserve uniquement le titre et le résumé de chaque article ;
* utilise les 250 premiers caractères du texte lorsqu’aucun résumé n’est disponible ;
* limite la liste finale à huit articles ;
* parcourt les groupes d’articles retournés par l’API.

### Objectifs

* Réduire la quantité de texte transmise au modèle.
* Éviter d’injecter le contenu intégral des articles.
* Conserver les informations essentielles nécessaires à l’analyse.
* Contrôler le coût et la taille des requêtes envoyées au LLM.

---

## 4. Synthèse intermédiaire des actualités

**Fichier :** `backend/src/ai/todayNews.py`, fonction `summarize_today_news`

World News API peut retourner plusieurs articles portant sur des sujets proches.

Une génération intermédiaire est donc effectuée par le LLM afin de :

* regrouper les sujets similaires ;
* supprimer les redondances ;
* produire une synthèse concise ;
* limiter cette synthèse à dix lignes maximum.

Le contexte final construit par `build_today_news_prompt` contient ensuite :

* les titres et résumés des actualités brutes ;
* la synthèse intermédiaire produite par le modèle ;
* les règles d’utilisation de ce contexte.

### Objectifs

* Donner au modèle une vue d’ensemble rapide des sujets principaux.
* Faciliter le regroupement thématique.
* Réduire l’effet des informations répétitives.
* Conserver les données brutes afin que l’agent puisse revenir aux titres et aux résumés d’origine.

### Limite actuelle

La synthèse intermédiaire ne réduit pas, à elle seule, la taille totale du prompt final, car les actualités brutes et la synthèse sont toutes deux ajoutées au contexte.

Elle améliore surtout la lisibilité du contexte et fournit une vue condensée des informations.

La réduction effective de la taille du prompt provient principalement :

* de la limitation à huit articles ;
* de la conservation du titre et du résumé uniquement ;
* de la limitation du texte de remplacement à 250 caractères lorsqu’aucun résumé n’est disponible.

---

## 5. Prompt de génération de revue de presse

**Fichiers concernés :**

* `backend/src/ai/pressReviewAgent.py`
* `backend/src/routes/pressReviews.py`

L’agent de revue de presse est défini comme un journaliste spécialisé.

Lorsqu’une revue est demandée, le backend lui transmet :

* le sujet choisi par l’utilisateur ;
* la consigne d’analyser toute la conversation ;
* l’historique du chat au moyen de `message_history`.

### Choix effectués

* Définir clairement le rôle de l’agent.
* Demander une synthèse des sujets abordés dans la conversation.
* Regrouper les thèmes similaires.
* Produire une revue de presse structurée.
* Rester factuel et neutre.
* Ne pas inventer d’informations.
* Utiliser uniquement les informations présentes dans l’historique transmis.
* Générer des résumés pour les articles ou sujets évoqués.
* Produire une partie consacrée aux tendances et perspectives.

### Objectifs

* Obtenir une revue claire et exploitable.
* Limiter la génération aux informations réellement présentes dans la conversation.
* Réduire le risque d’ajout d’informations externes non vérifiées.
* Produire un résultat stable, facile à enregistrer et à afficher.
* Faciliter la transformation de la réponse en contenu Markdown.

---

## 6. Choix d’une sortie structurée avec Pydantic

**Fichier :** `backend/src/ai/pressReviewAgent.py`

La revue de presse utilise le modèle Pydantic `PressReviewOutput`.

Il contient les champs suivants :

* `title` : titre global proposé par le modèle ;
* `global_summary` : synthèse générale ;
* `article_summaries` : liste structurée de résumés ;
* `perspectives` : analyse des tendances et perspectives.

Chaque élément de `article_summaries` respecte également une structure définie par `ArticleSummary` :

* `title` ;
* `summary`.

### Objectifs

* Contrôler la forme de la réponse générée.
* Réduire les erreurs de format.
* Valider automatiquement la structure retournée par le modèle.
* Manipuler facilement les différentes parties de la revue côté backend.
* Transformer simplement la réponse en Markdown.
* Améliorer la fiabilité de l’affichage côté frontend.

### Particularité du backend actuel

Le champ `title` généré par l’agent fait partie de la sortie structurée, mais il n’est pas utilisé pour le titre final enregistré.

Dans `backend/src/routes/pressReviews.py`, le backend construit lui-même le titre final avec :

```python
formatted_title = (
    f"REVUE DE PRESSE {data.subject.upper()} - {formatted_date}"
)
```

Ce choix garantit un format de titre homogène pour toutes les revues de presse.

Le contenu Markdown utilise ensuite principalement :

* `output.global_summary` ;
* `output.article_summaries` ;
* `output.perspectives`.
