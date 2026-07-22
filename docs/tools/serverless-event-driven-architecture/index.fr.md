---
title: Architecture à événements déclenchés de manière sans serveur
description: Un modèle d’architecture où les applications répondent à des événements et s’agencent automatiquement sans gérer l’infrastructure, idéal pour les services natives nuage.
created: 2026-07-22
tags:
  - serverless
  - événements
  - architecture
status: brouillon
---

# Architecture à événements déclenchés de manière sans serveur

## Introduction

L'Architecture à événements déclenchés de manière sans serveur (SEDA) est un paradigme de conception qui permet de construire des applications en utilisant un ensemble de fonctions déconnectées qui s'exécutent en réponse à des événements, sans la nécessité pour le développeur d'application de gérer et de provisionner des serveurs. Cette approche permet aux développeurs de construire des applications scalables, hautement disponibles et à coûts réduits en se concentrant uniquement sur le code qui gère la logique métier.

## Caractéristiques clés

1. **Fonctions déconnectées** : Les fonctions sont sans état et isolées, permettant d'échelonner indépendamment les instances en fonction de la demande.
2. **Déclenchés par événements** : Les fonctions sont déclenchées par des événements tels que les appels d'API, mises à jour de la base de données ou services externes.
3. **Echelonnement automatique** : La plateforme échelle automatiquement le nombre d'instances d'une fonction en fonction de la demande.
4. **Pay-as-you-go** : On paie uniquement pour les ressources utilisées lorsque les fonctions s'exécutent, entraînant des économies de coûts.
5. **Sans état** : Chaque appel de fonction est indépendant, et les données sont gérées par des services externes tels que des bases de données ou des stockages.
6. **Scalabilité** : Les fonctions peuvent être échelonnées automatiquement en fonction du charge.

## Histoire

Le concept du calcul sans serveur a des racines dans le calcul dans le nuage et l’évolution des services d’infrastructure comme un service (IaaS) et des plateformes comme un service (PaaS). Le terme "sans serveur" a été popularisé par les premiers adoptants tels que AWS Lambda en 2014. AWS Lambda a été la première grande plateforme de cloud à offrir un service de calcul sans serveur géré. Depuis lors, d'autres fournisseurs de cloud tels que Google Cloud Functions, Azure Functions et Alibaba Cloud Functions ont introduit des services similaires.

## Cas d'utilisation

1. **Applications web et mobiles** : Gestion des interactions utilisateur, traitement des données et tâches en arrière-plan.
2. **Gates API** : Rute et gestion des requêtes d'API.
3. **Internet des objets (IoT)** : Traitement des données provenant de capteurs et de dispositifs.
4. **Traitement de données** : Traitement des données en temps réel, traitement des journaux et analyse.
5. **Automatisation** : Automatisation des flux de travail et des processus de manière scalable.
6. **Délivrance de contenu** : Serveur de contenu basé sur les requêtes des utilisateurs, tels que des images ou des vidéos.

## Installation

L'installation d'une architecture sans serveur à événements déclenchés typiquement implique la mise en place d'une plateforme de cloud sans serveur de la part d'un fournisseur, tel que AWS Lambda ou Azure Functions. Voici un guide général :

1. **Créez un compte** : Inscription au service du fournisseur de cloud.
2. **Configurez un environnement** : Installez les SDK et outils nécessaires, tels que la CLI AWS ou la CLI Azure.
3. **Initialisez le projet** : Utilisez les outils CLI du fournisseur pour initialiser un nouveau projet sans serveur.
4. **Configurez les fonctions** : Écrivez et configurez vos fonctions. Cela comprend la spécification des déclencheurs et des sources d'événements.
5. **Déployez les fonctions** : Déploiez vos fonctions dans l'environnement sans serveur du fournisseur de cloud.
6. **Testez les fonctions** : Testez les fonctions pour vous assurer qu'elles fonctionnent correctement.

### Exemple : Configuration AWS Lambda

1. **Créez un compte AWS** et connectez-vous.
2. **Installez la CLI AWS** : Assurez-vous que vous avez la CLI AWS installée et configurée.
3. **Initialisez un projet sans serveur** :

   ```bash
   serverless create --template aws-nodejs --path my-lambda-project
   cd my-lambda-project
   ```

4. **Configurez la fonction** : Éditez `handler.js` pour inclure votre logique métier.

   ```javascript
   exports.handler = (event, context, callback) => {
     const message = event.message;
     const response = {
       statusCode: 200,
       body: JSON.stringify({ message: `Processed: ${message}` }),
     };
     callback(null, response);
   };
   ```

5. **Déployez la fonction** :

   ```bash
   serverless deploy
   ```

6. **Testez la fonction** : Utilisez le console AWS Lambda ou l'API Gateway pour tester la fonction.

## Utilisation de base

1. **Déclenchez la fonction** : Les fonctions sont déclenchées par des événements. Par exemple, dans AWS Lambda, vous pouvez déclencher une fonction via un API Gateway, un événement planifié ou un événement S3.
2. **Écrivez le code de la fonction** : Utilisez le langage de programmation préféré (par exemple, Node.js, Python) pour écrire la logique métier. Voici un exemple simple en Python utilisant AWS Lambda :

   ```python
   import json

   def lambda_handler(event, context):
       # Parsez l'événement
       message = event['message']
       
       # Traitez le message
       result = f"Processed: {message}"
       
       # Retournez le résultat
       return {
           'statusCode': 200,
           'body': json.dumps(result)
       }
   ```

3. **Déployez la fonction** : Utilisez les outils CLI ou SDK du fournisseur pour déployer la fonction.
4. **Surveillez et déboguez** : Utilisez les outils de surveillance du fournisseur pour suivre la performance de la fonction et déboguer tout problème.

## Conclusion

L'Architecture à événements déclenchés de manière sans serveur offre un moyen flexible et à coûts réduits pour construire des applications scalables sans gérer les serveurs. En utilisant des fonctions déclenchées par événements, les développeurs peuvent se concentrer sur l'écriture de code qui gère la logique métier spécifique, tandis que le fournisseur de cloud gère l'infrastructure sous-jacente. Cette approche est idéale pour une large gamme d'applications, allant des services web simples aux pipelines de traitement de données complexes.