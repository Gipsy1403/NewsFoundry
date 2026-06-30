# Analyse de performance

## 1. Analyse de la performance actuelle

- L’application se compose d’un frontend Next.js et d’un backend FastAPI qui appelle des agents IA.
- La qualité des réponses dépend du modèle IA utilisé et de la pertinence du prompt envoyé.
- Le temps de réponse utilisateur est majoritairement impacté par les appels API backend/IA.
- La fluidité des interactions dépend de la rapidité du backend et du rendu du frontend.

Points faibles observables

- Le backend peut attendre des réponses externes longues avant de renvoyer le message.
- Le contexte de conversation envoyé au modèle peut être trop volumineux, ce qui ralentit le traitement.
- L’interface peut rester bloquée si aucune animation de chargement ou feedback n’est présent.
- L’absence de streaming provoque une attente sans message progressif pendant la génération.

## 2. Mesure et observation des performances

- Mesurer le temps de génération moyen des réponses
  - en enregistrant le temps entre la réception du message utilisateur et la réponse renvoyée par le backend.
- Mesurer l’impact de la longueur de conversation
  - en comparant les temps de réponse selon le nombre de messages envoyés dans le contexte.

Comment collecter ces mesures

- Ajouter des logs dans le backend FastAPI autour des appels IA.
- Enregistrer des traces dans un fichier ou une base de données légère.
- Ajouter des métriques côté frontend sur les temps de latence de requêtes fetch.

Outils possibles

- MLflow pour tracer les exécutions si le service IA est centralisé.
- Un outil de monitoring simple comme Prometheus/Grafana pour suivre les temps de réponse.
- Un système de logs structurés pour analyser les pannes et les latences.

## 3. Pistes d’amélioration de performance

### Amélioration du temps de réponse

- Problème : les appels IA sont souvent séquentiels et peuvent durer plusieurs secondes.
- Solution : paralléliser les appels non critiques ou dégager des temps de réponse clients plus courts.
- Exemple : utiliser `async`/`await` dans FastAPI pour lancer plusieurs requêtes en parallèle, ou retourner un accusé de réception rapide suivi d’une réponse différée.

### Optimisation des prompts et du contexte envoyé

- Problème : le modèle reçoit potentiellement trop d’historique ou des informations redondantes.
- Solution : nettoyer le contexte avant chaque requête pour ne garder que l’essentiel.
- Exemple : conserver uniquement les derniers messages ou les résumés de conversation plutôt que tout l’historique.

### Mise en cache de certaines réponses

- Problème : des requêtes similaires génèrent souvent des réponses proches.
- Solution : mettre en cache les réponses pour les prompts identiques ou très proches.
- Exemple : utiliser un cache en mémoire ou Redis pour stocker le résultat d’un prompt et le réutiliser pendant une durée limitée.

### Réduction de la taille du contexte conversationnel

- Problème : les performances se dégradent lorsque le contexte devient long.
- Solution : appliquer une stratégie de troncature ou de résumé automatique.
- Exemple : remplacer les anciens messages par un résumé textuel avant de les renvoyer au modèle.

### Optimisation des appels API

- Problème : le backend appelle des services externes sans gestion du timeout ou du circuit breaker.
- Solution : définir des timeouts raisonnables et une stratégie de repli.
- Exemple : configurer un timeout de 10 secondes pour les requêtes IA et renvoyer une erreur utilisateur claire si la source externe ne répond pas.

## 4. Amélioration de l’expérience utilisateur

- La fluidité perçue peut être améliorée par un feedback immédiat.
- Afficher un loader ou un état de saisie désactivé pendant le traitement aide l’utilisateur à comprendre que la demande est en cours.

### Streaming des réponses

- Le streaming permet d’afficher progressivement le texte généré par le modèle.
- Côté backend : ouvrir une route qui émet des morceaux de texte au fur et à mesure de leur production.
- Côté frontend : afficher chaque fragment de réponse dès qu’il arrive.

Comment l’implémenter

- Backend FastAPI
  - utiliser `StreamingResponse` ou `EventSourceResponse` pour envoyer des tokens partiels.
  - transformer les réponses de l’agent IA en flux.
- Frontend React
  - consommer le flux et ajouter les fragments au message affiché.
  - afficher un état de chargement pendant que le flux n’est pas terminé.

## 5. Suivi et monitoring (MLOps léger)

- Suivre les performances dans le temps permet de détecter les régressions.
- Un outil comme MLflow peut stocker des traces de requêtes IA, des métriques et des comparaisons de versions.

Métriques utiles

- temps de réponse backend
- temps de génération IA
- taille du contexte envoyé au modèle
- coût estimé des requêtes IA
- qualité des réponses si elle est mesurable (feedback utilisateur, score de cohérence)

Comment suivre

- Collecter des métriques dans un service centralisé ou un fichier de logs.
- Visualiser l’évolution des latences et des coûts.
- Prendre des décisions basées sur des seuils : par exemple, alerter si le temps de réponse dépasse 5 secondes.

## Conclusion

- Le projet peut gagner en performance en optimisant le contexte IA, en introduisant du caching et en mesurant les temps de réponse.
- L’expérience utilisateur s’améliore nettement avec du streaming et des retours visuels immédiats.
- Un monitoring léger permet de suivre l’impact des changements et de garder le service stable.

## 6. Évolution de l'architecture IA : intégration d'une RAG

### Limite actuelle

- La revue de presse est générée à partir de l'historique de la conversation et des articles récupérés pendant le chat.
- Lorsque le nombre d'articles devient important, il n'est plus possible de transmettre l'ensemble des informations au modèle sans augmenter fortement la taille du contexte.
- Cette limitation peut réduire la qualité de la synthèse lorsque de nombreuses sources sont disponibles.

### Solution proposée

Mettre en place une architecture **Retrieval-Augmented Generation (RAG)**.

Le principe consiste à indexer les articles récupérés dans une base vectorielle. Avant chaque génération de revue de presse, une recherche sémantique sélectionne uniquement les documents les plus pertinents, qui sont ensuite injectés dans le prompt envoyé au modèle.

### Exemple d'implémentation

- Générer un embedding pour chaque article récupéré via WorldNewsAPI.
- Stocker ces embeddings dans une base vectorielle, par exemple **pgvector** avec PostgreSQL ou **ChromaDB**.
- Effectuer une recherche des articles les plus proches de la requête utilisateur.
- Construire le prompt à partir des documents retrouvés plutôt qu'à partir de l'ensemble de l'historique.

### Bénéfices attendus

- amélioration de la pertinence des revues de presse ;
- réduction du risque d'hallucination en s'appuyant sur des documents réels ;
- possibilité de traiter un volume d'articles beaucoup plus important ;
- diminution de la taille du contexte envoyé au modèle.

### Mesures associées

Mesures à suivre :

- nombre moyen d'articles pris en compte pour une revue de presse ;
- taille moyenne du contexte envoyé au modèle ;
- temps moyen de génération d'une revue de presse ;
- évaluation qualitative de la pertinence des synthèses lors de tests utilisateurs.

Objectifs mesurables :

- maintenir un temps de génération inférieur à 5 secondes ;
- réduire la taille du contexte transmis tout en conservant la qualité des réponses ;
- améliorer la couverture des informations disponibles lorsque plusieurs dizaines d'articles sont récupérés.
