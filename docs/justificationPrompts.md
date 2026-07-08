
# Justification des choix de prompts

Le projet utilise deux agents IA principaux :

- un agent conversationnel pour répondre aux questions d'actualité ;
- un agent spécialisé pour générer une revue de presse structurée.


## Prompt de l'agent conversationnel

L'agent conversationnel est configuré comme un assistant spécialisé dans l'analyse et la synthèse d'actualités.

Choix effectués :

- le rôle de l'agent est clairement défini pour éviter des réponses trop générales ;
- l'agent doit utiliser l'outil `current_date` pour les questions liées à la date ;
- l'agent doit utiliser l'outil `search_news` lorsqu'une question nécessite des articles récents ;
- les réponses doivent s'appuyer sur les articles récupérés ;
- lorsque plusieurs articles sont trouvés, l'agent doit comparer les informations et faire ressortir les points communs.

Objectif :

- limiter les réponses inventées ;
- améliorer la pertinence des réponses ;
- guider le modèle vers une réponse factuelle ;
- utiliser les données récupérées par WorldNewsAPI comme source de contexte.


## Prompt de contexte au moment de la création d'un chat

Lorsqu'un nouveau chat est créé, le backend récupère des actualités récentes et construit un contexte initial.

Choix effectués :

- fournir au modèle un contexte dès le début de la conversation ;
- éviter que le modèle réponde uniquement avec ses connaissances internes ;
- améliorer la cohérence des réponses pendant la discussion ;
- stocker ce contexte dans le chat pour le réutiliser ensuite.

Objectif :

- rendre la conversation plus fiable ;
- conserver une base d'information commune pendant toute la discussion ;
- réduire le risque d'hallucination.


## Prompt de génération de revue de presse

L'agent de revue de presse reçoit une consigne spécifique : analyser toute la conversation et produire une revue structurée.

Choix effectués :

- définir le rôle de l'agent comme journaliste spécialisé ;
- demander une synthèse globale ;
- demander des résumés d'articles ;
- demander une partie perspectives ;
- imposer une réponse factuelle et neutre ;
- demander au modèle de ne pas inventer d'informations ;
- limiter la génération au contexte présent dans l'historique.

Objectif :

- obtenir une revue claire et exploitable ;
- produire un format stable côté backend ;
- faciliter l'affichage dans le frontend ;
- éviter que le modèle ajoute des informations non présentes dans la conversation.


## Synthèse des actualités avant l'injection dans le prompt

Le endpoint `/top-news` de WorldNewsAPI retourne un grand nombre d'articles, dont plusieurs peuvent traiter du même sujet. Afin de limiter la taille du prompt envoyé au modèle et d'éviter les redondances, une première génération est effectuée par le LLM.

Cette génération intermédiaire produit une synthèse concise des actualités récupérées. Le prompt système final contient ensuite à la fois les actualités brutes et cette synthèse, ce qui permet d'améliorer la pertinence des réponses tout en réduisant la quantité d'informations répétitives transmises au modèle.


## Choix d'une sortie structurée avec Pydantic

La revue de presse utilise un modèle de sortie structuré avec Pydantic :

- `title` ;
- `global_summary` ;
- `article_summaries` ;
- `perspectives`.

Ce choix permet :

- de contrôler la forme de la réponse générée ;
- de réduire les erreurs de format ;
- de transformer facilement la réponse en Markdown ;
- d'améliorer la fiabilité côté frontend.