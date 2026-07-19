---
title: Créer un Projet d'API REST Réel en TypeScript
description: Un guide complet pour la construction d'une API REST solide en utilisant TypeScript, Express.js et MongoDB.
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - API REST
  - Authentification
  - Docker
status: brouillon
---

# Créer un Projet d'API REST Réel en TypeScript

Ce guide vous guide à travers le processus de construction d'une API REST solide en utilisant TypeScript, Express.js et MongoDB. Il comprend une documentation détaillée, des bonnes pratiques et des exemples de monde réel pour vous aider à comprendre et à implémenter une solution d'API prête à l'emploi.

## Fonctionnalités Clés

1. **TypeScript**: Typage statique pour une meilleure détection d'erreurs et une qualité de code améliorée.
2. **Express.js**: Un framework de application web populaire en Node.js.
3. **MongoDB**: Une base de données NoSQL documentaire pour le stockage de données.
4. **Authentification JWT**: Authentification sécurisée en utilisant les Tokens Web JSON (JWT).
5. **Mongoose**: Une bibliothèque ODM (Object Data Modeling) pour MongoDB.
6. **Testage**: Tests unitaires et d'intégration avec Jest et Supertest.
7. **Documentation Swagger**: Documentation de l'API auto-générée pour une référence facile.

## Installation

1. **Cloner le Répertoire**:
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **Installer les Dépendances**:
   ```sh
   npm install
   ```

3. **Configurer MongoDB**:
   - Installer MongoDB si ce n'est pas déjà fait.
   - Lancer le serveur MongoDB.
   - Configurer la chaîne de connexion dans le fichier `.env`.

4. **Configurer les Variables d'Environnement**:
   - Mettre à jour le fichier `.env` avec les variables d'environnement nécessaires, telles que la chaîne de connexion de la base de données, le secret JWT, etc.

5. **Lancer le Serveur**:
   ```sh
   npm start
   ```

## Utilisation de Base

### Points de Fin API

1. **Gestion des Utilisateurs**:
   - **Créer un Utilisateur**: POST `/api/users`
   - **Obtenir un Utilisateur**: GET `/api/users/:id`
   - **Mettre à jour un Utilisateur**: PATCH `/api/users/:id`
   - **Supprimer un Utilisateur**: DELETE `/api/users/:id`

2. **Gestion des Produits**:
   - **Créer un Produit**: POST `/api/products`
   - **Obtenir un Produit**: GET `/api/products/:id`
   - **Mettre à jour un Produit**: PATCH `/api/products/:id`
   - **Supprimer un Produit**: DELETE `/api/products/:id`

3. **Gestion des Commandes**:
   - **Créer une Commande**: POST `/api/orders`
   - **Obtenir une Commande**: GET `/api/orders/:id`
   - **Mettre à jour une Commande**: PATCH `/api/orders/:id`
   - **Supprimer une Commande**: DELETE `/api/orders/:id`

4. **Authentification**:
   - **Générer un Token JWT**: POST `/api/auth/login`
   - **Protéger les Routes**: Utiliser un token JWT dans la tête d'autorisation

### Testage

1. **Testage Unitaire**:
   - Utiliser Jest pour le test unitaire.
   - Exécuter les tests avec:
     ```sh
     npm test
     ```

2. **Testage d'Intégration**:
   - Utiliser Supertest pour le test d'intégration.
   - Exécuter les tests avec:
     ```sh
     npm test
     ```

### Documentation Swagger

1. **Accéder à Swagger UI**:
   - Naviguer vers `http://localhost:3000/docs` dans votre navigateur.
   - Utiliser la documentation générée pour comprendre et interagir avec l'API.

### Authentification

1. **Générer un Token JWT**:
   - Effectuer une requête POST à `/api/auth/login` avec les identifiants de l'utilisateur.
   - Exemple en utilisant `curl`:
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **Inclure le JWT dans les Requêtes**:
   - Utiliser le JWT dans la tête d'autorisation pour les routes protégées.
   - Exemple en utilisant `curl`:
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### Gestion des Données

1. **Définir les Schémas Mongoose**:
   - Utiliser Mongoose pour définir des schémas pour les modèles.
   - Exemple de schéma pour un Utilisateur:
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **Effectuer des Opérations CRUD**:
   - Utiliser des méthodes Mongoose pour effectuer les opérations CRUD.
   - Exemple pour créer un utilisateur:
     ```typescript
     import { Request, Response } from 'express';
     import User from '../models/User';

     const createUser = async (req: Request, res: Response) => {
       const { name, email, password } = req.body;
       const user = new User({ name, email, password });
       await user.save();
       res.status(201).json(user);
     };
     ```

## Conclusion

En suivant le guide détaillé et en utilisant le code fourni comme point de départ, vous pouvez étendre et personnaliser l'API pour répondre aux besoins spécifiques de votre projet. Ce projet complet non seulement fournit un exemple pratique, mais sert également d'outil d'apprentissage excellent pour comprendre les bonnes pratiques de développement web modernes avec TypeScript, Express.js et MongoDB.

Bonne programmation !