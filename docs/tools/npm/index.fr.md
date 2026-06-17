---
title: npm - Gestionnaire de paquets Node
description: Un gestionnaire de paquets pour Node.js qui est un outil fondamental pour gérer les dépendances JavaScript.
created: 2026-06-14
tags:
  - package-manager
  - javascript
  - nodejs
  - cli
  - dependency-management
status: draft
ecosystem: javascript
---

# npm – Gestionnaire de paquets Node

npm (Node Package Manager) est le gestionnaire de paquets par défaut pour l'environnement d'exécution JavaScript Node.js. Il se compose de deux composants principaux : une **CLI** (interface en ligne de commande) pour gérer les dépendances et le **npm Registry**, une vaste base de données publique de paquets JavaScript. Il est devenu un outil essentiel dans l'écosystème JavaScript, permettant aux développeurs de partager, réutiliser et gérer du code efficacement.

## Qu'est-ce que npm ?

npm offre la possibilité de :

- **Installer et gérer les dépendances** – suivre les paquets dans `package.json` et les lock files.
- **Publier des paquets** – partager vos propres bibliothèques avec la communauté ou votre organisation.
- **Exécuter des scripts** – automatiser les workflows de construction, de test et de déploiement.
- **Gérer des monorepos** – en utilisant les workspaces pour gérer plusieurs paquets dans un seul dépôt.

## Pourquoi utiliser npm ?

- **Standardisation** – npm est fourni avec Node.js, ce qui en fait le choix par défaut pour la plupart des projets JavaScript.
- **Écosystème vaste** – plus de 2 millions de paquets dans le registre, couvrant pratiquement tous les besoins.
- **Reproductibilité** – le fichier `package-lock.json` garantit des installations déterministes dans tous les environnements.
- **Sécurité** – `npm audit` vous aide à trouver et corriger les vulnérabilités dans votre arbre de dépendances.
- **Pratique** – `npx` permet d'exécuter des paquets sans installation globale, et les scripts simplifient les tâches courantes.

## Installation

npm est installé automatiquement avec Node.js. Pour obtenir la dernière version LTS :

1. Téléchargez Node.js depuis [nodejs.org](https://nodejs.org/).
2. Vérifiez l'installation :

```bash
node -v
npm -v
```

### Installer via un gestionnaire de versions (nvm/fnm)

L'utilisation d'un gestionnaire de versions vous permet de basculer entre les versions de Node.js et d'installer npm pour chacune :

```bash
# Example with nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

Après l'installation, npm est prêt à être utilisé.

## Utilisation de base

### Initialiser un projet

Créez un nouveau projet ou convertissez un dossier existant :

```bash
npm init -y
```

Ceci génère un fichier `package.json` avec des valeurs par défaut. Utilisez `npm init` (sans `-y`) pour une invite interactive.

### Installer des dépendances

```bash
# Production dependency
npm install lodash

# Dev-only dependency
npm install --save-dev jest

# Global package (use sparingly; prefer npx)
npm install -g nodemon

# Install all dependencies from package.json
npm install
```

### Installer des versions spécifiques

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### Exécuter des scripts

Les scripts sont définis sous la clé `"scripts"` dans `package.json`. Raccourcis courants :

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### Désinstaller des paquets

```bash
npm uninstall lodash
```

### Mettre à jour des paquets

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### Vérifier les vulnérabilités

```bash
npm audit
```

Pour corriger automatiquement (lorsque disponible) :

```bash
npm audit fix
```

### Installation propre pour CI

```bash
npm ci
```

`npm ci` est plus rapide et supprime `node_modules` avant d'installer exactement à partir de `package-lock.json`.

## Fonctionnalités clés

### npx – Exécuter des paquets sans installation

`npx` est fourni avec npm et vous permet d'exécuter des binaires depuis le registre sans installation globale :

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

Si le paquet est déjà installé localement, `npx` utilisera cette version.

### Workspaces (support des monorepos)

Les workspaces npm vous permettent de gérer plusieurs paquets dans un seul dépôt :

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

Ensuite, exécutez des commandes sur tous les workspaces :

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

La liaison entre les paquets des workspaces est gérée automatiquement.

### Hooks de cycle de vie des scripts

npm fournit des hooks pré/post pour les scripts courants :

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

Exemple :

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

Ce fichier verrouille la version exacte de chaque dépendance et de ses dépendances transitives. Il garantit que toute personne exécutant `npm install` obtienne la même arborescence, rendant les constructions reproductibles.

### Overrides et résolutions

Vous pouvez forcer des versions spécifiques de dépendances transitives dans `package.json` :

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

Ceci est utile lorsqu'une sous-dépendance présente une vulnérabilité que vous devez corriger sans attendre la publication de sa dépendance parente.

### npm config

Personnalisez le comportement de npm globalement ou par projet :

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

Vous pouvez également utiliser un fichier `.npmrc` à la racine du projet.

### Paquets globaux vs npx

Les installations globales doivent être réservées aux outils que vous utilisez dans de nombreux projets (par exemple, `npm`, `yarn`, `node-gyp`). Pour les commandes ponctuelles, préférez `npx` pour éviter de polluer l'espace de noms global et garantir que vous utilisez toujours la version souhaitée.

## Conclusion

npm est un outil puissant et essentiel pour tout développeur JavaScript. De l'installation simple de dépendances à la gestion complexe de monorepos, son riche ensemble de fonctionnalités aide à garder les projets organisés, sécurisés et reproductibles. Que vous construisiez une petite bibliothèque ou une grande application, maîtriser npm améliorera considérablement votre flux de travail.