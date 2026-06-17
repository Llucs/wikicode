---
title: Postman - Plateforme de développement et de test d'API
description: Un guide complet sur Postman, la plateforme API standard de l'industrie pour concevoir, construire, tester et documenter les API.
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - Plateforme de développement et de test d'API

## Qu'est-ce que Postman ?

Postman est une plateforme API complète qui simplifie chaque étape du cycle de vie des API – de la conception et du développement aux tests, à la documentation et à la surveillance. Initialement conçu comme un simple client HTTP, il a évolué en un environnement collaboratif utilisé par des millions de développeurs et d'ingénieurs QA dans le monde entier. Postman prend en charge les protocoles REST, GraphQL et SOAP, et offre un riche ensemble d'outils pour construire et travailler avec des API de manière efficace.

## Pourquoi utiliser Postman ?

- **Client HTTP complet :** Envoyez facilement des requêtes de n'importe quelle méthode, personnalisez les en-têtes, l'authentification et le contenu du corps.
- **Outils d'organisation :** Regroupez les requêtes en collections, gérez les variables avec les environnements, et réutilisez les données dans tout un espace de travail.
- **Scripts et tests :** Écrivez des scripts de test JavaScript pour automatiser les assertions, extraire des données entre les requêtes et gérer des flux de travail dynamiques.
- **Prêt pour l'automatisation :** Utilisez le Collection Runner pour des exécutions manuelles ou Newman pour une exécution sans tête (CI/CD, pipelines).
- **Collaboration :** Partagez des collections et des environnements via des espaces de travail cloud avec contrôle de version et commentaires.
- **Documentation et maquettes :** Générez automatiquement la documentation des API et des serveurs de simulation pour simuler les réponses des API avant que le backend ne soit prêt.
- **Surveillance :** Mettez en place des moniteurs pour planifier des exécutions de collections et vérifier l'état des API.

## Installation

### Application de bureau (recommandée)

Postman propose des applications de bureau natives pour Windows, macOS et Linux.

- Téléchargez l'installateur approprié depuis [getpostman.com](https://getpostman.com)
- Alternativement, utilisez la **version web** sur [go.postman.co](https://go.postman.co) avec l'agent de bureau pour gérer les appels API.

### Newman (CLI pour CI/CD)

Newman est l'exécuteur de collections en ligne de commande pour Postman. Il vous permet d'exécuter et de tester une collection Postman directement depuis la ligne de commande, ce qui le rend idéal pour intégrer les tests API dans votre pipeline de développement.

Installez via npm :

```bash
npm install -g newman
```

Ou avec Yarn :

```bash
yarn global add newman
```

## Utilisation de base

1. **Créer une requête**  
   Cliquez sur le bouton **Nouveau** et choisissez **Requête HTTP** (ou utilisez `Ctrl+N`).

2. **Spécifier la requête**  
   - Saisissez l'URL (par ex. `https://jsonplaceholder.typicode.com/posts`)  
   - Sélectionnez la méthode HTTP (`GET`, `POST`, `PUT`, etc.)  
   - Ajoutez les en-têtes, paramètres de requête ou corps de requête nécessaires.

3. **Envoyer et inspecter**  
   Cliquez sur **Envoyer**. Le panneau de réponse affiche le code de statut, le temps de réponse, les en-têtes et le corps.

4. **Enregistrer dans une collection**  
   Cliquez sur **Enregistrer** et créez une nouvelle collection ou ajoutez à une collection existante.

5. **Ajouter un test**  
   Sous l'onglet **Tests**, écrivez un script JavaScript pour valider la réponse. Exemple :

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   Réexécutez la requête – le résultat du test apparaît dans l'onglet **Résultats des tests**.

## Fonctionnalités clés avec des exemples

### 1. Collections

Les collections vous aident à regrouper des requêtes connexes et à les partager avec votre équipe. Une collection peut également inclure des dossiers et des métadonnées.

```javascript
// Example of using collection variables in a pre-request script
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

Exécutez une collection entière avec Newman :

```bash
newman run MyCollection.json
```

### 2. Environnements

Les environnements contiennent des paires clé-valeur pour les variables qui changent entre les configurations (développement, préproduction, production).

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

Utilisez `{{base_url}}` dans vos URL de requête. Basculez entre les environnements pour changer de contexte instantanément.

### 3. Scripts de pré-requête et de test

Les scripts Postman sont écrits en JavaScript et s'exécutent dans un bac à sable avec accès aux objets fournis par Postman comme `pm`.

**Script de pré-requête** (exécuté avant l'envoi de la requête) :

```javascript
// Dynamically set a timestamp parameter
pm.variables.set("timestamp", Date.now());
```

**Script de test** (exécuté après la réception de la réponse) :

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. Collection Runner

Exécutez une collection entière ou un dossier plusieurs fois avec des fichiers de données.

- Ouvrez **Runner** en haut à gauche de Postman.
- Sélectionnez une collection, choisissez un environnement, définissez les itérations.
- Vous pouvez fournir un fichier de données CSV ou JSON pour injecter des données dans chaque itération.

### 5. Newman – Intégration en ligne de commande

Newman vous permet d'intégrer vos tests Postman dans des pipelines CI/CD (Jenkins, GitLab CI, GitHub Actions, etc.).

**Exécutez une collection avec un environnement et un fichier de données :**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

Le rapporteur `htmlextra` génère un rapport HTML interactif de l'exécution des tests.

**Utilisation dans un script Node.js :**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. Génération de documentation

Postman peut générer automatiquement de la documentation pour toute collection. Ouvrez simplement une collection, cliquez sur le menu **...** et choisissez **Voir la documentation**. La documentation comprend des exemples de requêtes, des schémas de requête/réponse et des extraits de code dans divers langages.

Publiez la documentation sur le web via le bouton **Publier la documentation**, ou exportez-la au format HTML.

### 7. Serveurs de simulation

Mimez une API en créant un serveur de simulation à partir de votre collection. C'est extrêmement utile pour le développement frontend lorsque le backend n'est pas encore prêt.

- Sélectionnez une collection, cliquez sur **Serveurs de simulation**.
- Postman crée une URL de serveur de simulation qui renvoie les exemples de réponses enregistrés.

### 8. Moniteurs

Les moniteurs vous permettent de planifier des exécutions périodiques d'une collection sur l'infrastructure cloud de Postman. Vous recevez des alertes si des tests échouent.

- Allez dans **Moniteurs** → **Créer un moniteur**.
- Sélectionnez une collection, définissez une fréquence (par exemple toutes les heures), et éventuellement définissez des alertes (email, Slack, etc.).

## Résumé

Postman est bien plus qu'un client API – c'est une plateforme à part entière qui prend en charge l'ensemble du cycle de vie des API. De la simulation initiale et de la conception collaborative aux tests automatisés via Newman et à la surveillance en production, Postman dote les équipes d'une source unique de vérité pour leurs API. Sa facilité d'utilisation, combinée à des scripts puissants et à l'intégration CI/CD, en fait un outil indispensable pour les flux de travail de développement modernes.