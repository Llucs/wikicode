---
title: DBGate
description: DBGate est un outil de gestion de base de données open-source, multiplateforme, basé sur le web pour MySQL, PostgreSQL, SQL Server, MongoDB, SQLite et plus, offrant une interface moderne pour l'administration et le développement de bases de données.
created: 2026-06-20
tags:
  - database
  - open-source
  - web-based
  - tool
  - management
status: draft
---

# DBGate

DBGate est un outil de gestion de base de données open-source (MIT), basé sur le web, conçu comme une alternative moderne aux outils classiques tels que phpMyAdmin, Adminer, DBeaver ou DataGrip. Construit avec un backend Node.js/Express et un frontend React, il offre une interface utilisateur propre et moderne qui fonctionne entièrement dans un navigateur web, ce qui le rend multiplateforme et idéal pour les environnements cloud, serveur et conteneurisés.

## Pourquoi DBGate ?

Les clients de base de données traditionnels nécessitent souvent une installation sur le système d'exploitation, ce qui entraîne une fragmentation entre les équipes et les environnements. DBGate résout ce problème en étant entièrement basé sur le navigateur, vous permettant de :

- **Gérer les bases de données à distance** sans avoir besoin de tunnels SSH ou de clients natifs.
- **Intégrer dans des stacks Docker** pour un accès instantané aux bases de données de développement.
- **Partager les connexions et les scripts** via une instance centralisée (avec authentification).
- **Travailler de manière transparente sur Windows, macOS et Linux** en utilisant la même interface web.

## Fonctionnalités clés

| Feature | Description |
|---------|-------------|
| Support multi-bases de données | Connectez-vous simultanément à MySQL, MariaDB, PostgreSQL, SQL Server, MongoDB, SQLite, CockroachDB, Amazon Redshift et Redis. |
| Éditeur SQL avancé | Coloration syntaxique, auto-complétion intelligente, requêtes multi-onglets et historique complet des requêtes. |
| Navigateur de schéma/données | Parcourez, créez, modifiez et supprimez des objets de base de données. Édition de données en ligne avec un tri et un filtrage puissants. |
| Diagrammes ER | Générez automatiquement des diagrammes entité-relation pour visualiser les schémas de base de données. |
| Exportation/Importation | Exportez vers CSV, JSON, SQL, Markdown, Excel ; importez à partir de fichiers CSV et SQL. |
| Navigation par clé étrangère | Accédez directement aux enregistrements liés depuis le navigateur de données. |
| Surveillance du serveur | Affichez les processus actifs, l'état du serveur et les configurations de variables |
| Optimisé pour Docker | Image Docker officielle pour un déploiement facile sur n'importe quel serveur. |
| Application de bureau | Version Electron intégrée pour une utilisation autonome sur Windows, macOS et Linux. |

## Installation

DBGate peut être installé et exécuté de plusieurs manières :

### 1. Docker (Recommandé pour le serveur)

```bash
docker run -d -p 3000:3000 --name dbgate dbgate/dbgate
```

Accédez ensuite à `http://localhost:3000`.

Pour une configuration avec `docker-compose.yml` :

```yaml
version: '3'
services:
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    restart: unless-stopped
```

### 2. Node Package Manager (NPM)

```bash
npm install -g dbgate
dbgate
```

Accédez via `http://localhost:3000`.

### 3. Installateur de bureau

Téléchargez les installateurs pré-construits pour Windows, macOS et Linux depuis la [page des versions GitHub](https://github.com/dbgate/dbgate/releases).

### 4. Déploiements cloud

Des options de déploiement en un clic sont disponibles pour Heroku, Railway et les plateformes similaires.

## Démarrage rapide / Utilisation

### 1. Lancer DBGate

Accédez à `http://localhost:3000` dans votre navigateur.

### 2. Ajouter une connexion

Cliquez sur l'icône **+** à côté de **Connexions**. Choisissez votre moteur de base de données (par exemple, PostgreSQL), et saisissez les informations de connexion : Hôte, Port, Nom d'utilisateur, Mot de passe, Base de données.

### 3. Parcourir les données

Cliquez sur la connexion enregistrée pour voir une arborescence des bases de données/tables. Cliquez sur une table pour voir ses lignes.

### 4. Interroger la base de données

Cliquez sur le bouton **Requête** pour ouvrir l'éditeur SQL. Écrivez votre SQL et appuyez sur **Exécuter** (ou `Ctrl+Enter`).

### 5. Visualiser le schéma

Faites un clic droit sur une base de données ou une table et sélectionnez **Diagramme ER** pour générer un schéma visuel.

### 6. Exporter les données

Faites un clic droit sur une table ou un jeu de résultats et sélectionnez **Exporter** pour télécharger les données dans le format de votre choix (CSV, JSON, SQL, etc.).

## Exemples de commandes

**Lancer DBGate avec Docker et persister les données :**

```bash
docker run -d \
  -p 3000:3000 \
  -v dbgate-data:/home/app/.dbgate \
  --name dbgate \
  dbgate/dbgate
```

**Utiliser avec une instance PostgreSQL locale dans une stack de développement :**

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    depends_on:
      - postgres
```

**Installer et exécuter avec npm :**

```bash
npm install -g dbgate
dbgate
```

**Se connecter en utilisant des variables d'environnement (avancé) :**

```bash
docker run -d \
  -e DBGATE_SERVER_NAME=myPostgres \
  -e DBGATE_SERVER_TYPE=postgres \
  -e DBGATE_SERVER_HOST=192.168.1.100 \
  -e DBGATE_SERVER_PORT=5432 \
  -e DBGATE_SERVER_USER=admin \
  -e DBGATE_SERVER_PASSWORD=secret \
  -p 3000:3000 \
  dbgate/dbgate
```

## Cas d'utilisation

1. **Administration de serveur distant** – Gérez les bases de données sur un VPS ou une instance cloud sans tunneling SSH ni installation de clients natifs.
2. **Environnements de développement** – Incluez DBGate dans une stack `docker-compose.yml` pour offrir aux développeurs un accès GUI instantané à leurs bases de données locales.
3. **Outils d'équipe** – Déployez une instance centralisée de DBGate (avec authentification appropriée) pour qu'une équipe puisse partager l'accès aux bases de données de développement ou de préproduction.
4. **Éducation et formation** – Fournissez rapidement aux étudiants une interface SQL sans gérer les installations de clients.
5. **Flux de travail multiplateformes** – Basculez de manière transparente entre les systèmes d'exploitation en utilisant la même interface web.

## Architecture

DBGate se compose de :

- **Backend :** Serveur Node.js/Express traitant les connexions aux bases de données, l'exécution des requêtes et les points d'API.
- **Frontend :** SPA basée sur React fournissant l'interface utilisateur, comprenant l'éditeur SQL, le navigateur de données et le visualiseur de schéma.
- **Pilotes de base de données :** Prend en charge plusieurs moteurs de base de données via des pilotes Node.js natifs ou des ponts ODBC/JDBC.

L'application stocke les connexions, les scripts SQL et d'autres objets dans le stockage local (ou un stockage cloud optionnel pour la version hébergée). L'image Docker regroupe toutes les dépendances pour un déploiement sur un seul port.

## Limitations

- **Fonctionnalités avancées d'IDE :** Peut manquer certaines fonctionnalités présentes dans IntelliJ DataGrip (par exemple, refactorisation distribuée, analyse de code avancée).
- **Performances :** Le rendu de très grands ensembles de données (>100k lignes) dans le navigateur peut être plus lent que les applications natives. Les opérations d'exportation sont traitées côté serveur pour de meilleures performances.
- **Authentification :** La version open-source n'inclut pas d'authentification utilisateur intégrée ; vous devez la placer derrière un proxy inverse (comme nginx + auth_basic) pour une utilisation en équipe.

## Résumé

DBGate est un outil de gestion de base de données puissant, flexible et open-source qui comble le fossé entre les clients web légers (comme phpMyAdmin) et les IDE natifs lourds (comme DataGrip). Sa nature multiplateforme, sa conception adaptée aux conteneurs et son ensemble de fonctionnalités en pleine croissance en font un excellent choix pour les développeurs, les administrateurs de bases de données et les équipes à la recherche d'un client de base de données moderne et natif du web.

---

*Document généré le 2026-06-20. Visitez le [dépôt officiel](https://github.com/dbgate/dbgate) pour les dernières mises à jour.*