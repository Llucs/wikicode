---
title: DBeaver - Outil universel de gestion de base de données
description: Un outil de gestion de base de données gratuit, open-source et multiplateforme, ainsi qu'un client SQL pour les développeurs, les administrateurs de bases de données et les analystes de données.
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - Outil universel de gestion de base de données

## Aperçu

DBeaver est un outil de gestion de base de données et un client SQL **gratuit, open-source et multiplateforme**. Il fournit une interface graphique riche pour interagir avec toute base de données prenant en charge les pilotes JDBC ou ODBC, ce qui en fait un outil universel pour les développeurs, les administrateurs de bases de données et les analystes de données.

- **Licence** : La version Community (CE) est publiée sous licence **Apache 2.0** ; des éditions commerciales Pro/Enterprise/Team sont également disponibles.
- **Plateforme** : Windows, macOS, Linux (également disponible en version portable).
- **Architecture** : Construit sur la plateforme Eclipse Rich Client Platform (RCP) en utilisant Java.
- **Historique** : Initié en 2010 par Serge Rielau, un expert en bases de données ayant précédemment travaillé sur Apache Derby et Oracle. Le projet a rapidement gagné en adoption, menant à la création de DBeaver Corp.

DBeaver est idéal pour :
- **Développement d'applications** – Écrire, déboguer et optimiser des requêtes SQL.
- **Administration de bases de données** – Gérer les schémas, utilisateurs, sessions et index.
- **Analyse de données** – Exécuter des requêtes analytiques et exporter les résultats vers différents formats.
- **Ingénierie des données** – Transférer des données entre différentes bases de données sans scripts lourds.
- **Éducation** – Apprendre SQL et les concepts de bases de données relationnelles via une interface graphique intuitive.

## Fonctionnalités clés

| Fonctionnalité | Description |
|---------|-------------|
| **Prise en charge étendue des bases de données** | Se connecte à plus de 100 bases de données prêtes à l'emploi, notamment MySQL/MariaDB, PostgreSQL, Oracle, SQL Server, SQLite, DB2, Snowflake, Redshift, ClickHouse, et bien d'autres. |
| **Éditeur SQL avancé** | Coloration syntaxique, complétion de code, exécution de requêtes avec plusieurs onglets de résultats, visualisation du plan d'exécution (graphique), formatage SQL et requêtes paramétrées. |
| **Navigateur de données / Tableur** | Édition en ligne puissante, filtrage avancé, tri et gestion des données BLOB/CLOB directement dans une interface de grille. |
| **Diagrammes ER** | Génération automatique de diagrammes Entité-Relation avec rétro-ingénierie (clic droit sur un schéma ou une table). |
| **Gestion des schémas** | Explorateur d'objets pour parcourir, créer et modifier tables, vues, index, procédures et fonctions. |
| **Transfert de données** | Export/import en masse entre bases de données et formats de fichiers (CSV, JSON, XML, Excel, SQL, Markdown, HTML). |
| **Outils d'administration** | Gestionnaire de sessions, planificateur de tâches (Pro), gestion des utilisateurs/rôles et tunneling SSH/SSL/Proxy intégré. |
| **Extensibilité** | Architecture de plugins ; plugin disponible pour pilotes supplémentaires, contrôle de version (Git) et personnalisations de diagrammes. |
| **Multiplateforme** | Fonctionne sur Windows, macOS et Linux. |

## Installation

DBeaver est disponible via plusieurs canaux. Choisissez la méthode qui correspond à votre environnement.

### Installateur officiel (toutes les plateformes)

Téléchargez l'installateur pour votre système d'exploitation depuis [dbeaver.io](https://dbeaver.io) (Community Edition) ou [dbeaver.com](https://dbeaver.com) (Enterprise).

### Gestionnaires de paquets

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – Dépôts officiels Debian/RPM)**
```bash
# Debian/Ubuntu
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt update && sudo apt install dbeaver-ce

# RHEL/CentOS/Fedora
sudo rpm --import https://dbeaver.io/rpms/dbeaver.gpg.key
sudo yum install dbeaver-ce
```

**Windows (winget / Chocolatey)**
```powershell
# winget (Windows 10 / 11)
winget install DBeaver.DBeaverCE

# Chocolatey
choco install dbeaver
```

**Version portable Windows**

Un exécutable portable est disponible sur le site officiel, idéal pour une utilisation depuis une clé USB sans installation.

## Prise en main – Utilisation de base

### 1. Créer une connexion à une base de données

1. Lancez DBeaver.
2. Cliquez sur le bouton **Nouvelle connexion à une base de données** (icône de prise) dans la barre d'outils.
3. Sélectionnez votre type de base de données (par exemple, **PostgreSQL**).
4. Remplissez les détails de connexion :
   - Hôte, Port, Nom de la base de données, Nom d'utilisateur, Mot de passe.
5. Cliquez sur **Tester la connexion**. DBeaver vous invitera automatiquement à télécharger le pilote JDBC nécessaire s'il n'est pas déjà en cache.
6. Cliquez sur **Terminer**. La connexion apparaît dans le panneau **Database Navigator**.

![Exemple d'assistant de connexion](https://dbeaver.com/docs/images/connection-wizard.png) <!-- URL de substitution ; la documentation réelle fournit des captures d'écran -->

### 2. Parcourir et interroger les données

- Dans le **Database Navigator**, développez une connexion pour voir les schémas, tables, vues, etc.
- Faites un clic droit sur une table et sélectionnez **View Data** pour ouvrir une grille de données.
- Pour écrire du SQL personnalisé, appuyez sur `Ctrl + ]` (Windows/Linux) ou `Cmd + ]` (macOS) pour ouvrir un nouvel **SQL Editor**.

**Exemple de requête SQL :**
```sql
-- Select users with their latest order
SELECT u.id, u.name, o.order_date
FROM users u
JOIN (
    SELECT user_id, MAX(order_date) AS order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
ORDER BY o.order_date DESC;
```

- Exécutez la requête avec `Ctrl + Enter` (Win/Lin) ou `Cmd + Enter` (macOS).
- Les résultats apparaissent dans la grille de résultats sous l'éditeur.

### 3. Modifier et exporter les données

- Cliquez directement sur une cellule dans la grille de résultats pour la modifier (nécessite la permission **Edit** sur la table).
- Faites un clic droit sur la grille de résultats et choisissez **Export Data**.
- Sélectionnez le format souhaité (CSV, Excel, JSON, SQL INSERT, XML, Markdown, etc.) et configurez les options.

## Utilisation avancée

### Diagrammes Entité-Relation (ER)

DBeaver peut générer des diagrammes ER pour un schéma ou des tables spécifiques.

1. Faites un clic droit sur un schéma dans le Database Navigator.
2. Sélectionnez **View Diagram** (ou ouvrez l'onglet **ER Diagram**).
3. Le diagramme affiche les tables, colonnes, relations et index.
4. Vous pouvez réorganiser les éléments, exporter le diagramme en tant qu'image ou l'imprimer.

### Transfert de données / Migration

Utilisez l'assistant **Transfer Data** pour copier des données entre bases de données ou extraire des données vers des fichiers.

1. Faites un clic droit sur une table ou un schéma.
2. Sélectionnez **Data > Transfer Data**.
3. Choisissez la source (par exemple, une table) et la cible (une autre connexion à une base de données ou un fichier).
4. Configurez les correspondances de colonnes et les règles de transformation.
5. Exécutez le transfert.

### Plan d'exécution (EXPLAIN)

Visualisez le plan d'exécution des requêtes pour l'optimisation SQL.

1. Dans le SQL Editor, écrivez une requête.
2. Cliquez sur le bouton **Explain Plan** (ou faites un clic droit → **Explain Plan**).
3. DBeaver affiche un plan graphique avec les détails de coût et l'utilisation des index.

### Outil de comparaison (Pro/Enterprise)

Les outils **Structure Compare** et **Data Compare** vous permettent de comparer les schémas ou les données entre deux bases de données ou environnements.

- Disponible dans les éditions commerciales.

## Configuration et personnalisation

### Paramètres de connexion

- **Propriétés du pilote** : Modifiez les attributs du pilote JDBC (par exemple, délais d'attente, mode SSL, tailles de bloc) à partir de l'éditeur de connexion.
- **Tunnel SSH** : Configurez le tunneling SSH pour un accès sécurisé aux bases de données distantes (dans l'onglet **SSH** des paramètres de connexion).
- **SSL** : Activez SSL et importez des certificats via l'onglet **SSL**.

### Préférences globales

- `Window → Preferences` (Windows/Linux) ou `DBeaver → Preferences` (macOS).
- **Apparence** : Basculez entre les thèmes clair/foncé, ajustez les tailles de police.
- **Éditeurs** : Configurez le style de formatage SQL, le comportement de l'auto-complétion et les options d'exécution.
- **Connexions** : Définissez les niveaux d'isolation des transactions par défaut, l'auto-commit et les délais d'inactivité.

### Gestion des pilotes

- **Gestionnaire de pilotes** : `Database → Driver Manager`. Affichez, modifiez ou ajoutez des pilotes JDBC personnalisés.
- Téléchargez les pilotes manquants directement depuis le dépôt de pilotes de DBeaver lors de la première connexion à une base de données.

## Automatisation et écriture de scripts

### DBeaver CLI (Pro/Enterprise uniquement)

DBeaver Pro/Enterprise inclut un outil en ligne de commande (`dbeaver-cli`) pour exécuter des scripts SQL, exporter des données ou exécuter des tâches sans interface graphique.

```bash
# Connect and run a script against a PostgreSQL instance
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### Planificateur de tâches (Pro/Enterprise)

Planifiez des exportations récurrentes, des transferts de données ou des scripts SQL à l'aide du planificateur intégré (interface de type cron).

## Intégrations

- **Contrôle de version** : Plugin d'intégration Git (disponible dans Community) – validez des scripts SQL ou comparez avec des versions validées.
- **Docker** : L'exécution de DBeaver directement dans un conteneur pour les pipelines CI/CD est possible avec l'édition CLI.
- **Bases de données cloud** : Pilotes pré-configurés pour Snowflake, Amazon Redshift, Google BigQuery, Azure SQL, etc.
- **SSH/SSL** : Prise en charge intégrée des connexions sécurisées et de l'authentification proxy.

## Compatibilité et performances

| Aspect | Détails |
|--------|---------|
| **Systèmes d'exploitation pris en charge** | Windows 10+, macOS 10.15+, Linux (x64, amd64, aarch64) |
| **Prérequis Java** | JDK 11 ou ultérieur (inclus avec les installateurs) |
| **Prise en charge des bases de données** | 100+ bases de données via JDBC/ODBC (incluant relationnelles, type NoSQL, cloud) |
| **Conseils de performance** | - Utilisez des index pour les grandes requêtes.<br>- Fermez les connexions inactives dans les préférences.<br>- Activez **« Utiliser les mises à jour par lots »** pour les opérations en masse.<br>- Pour des ensembles de données extrêmement volumineux, exportez par morceaux ou utilisez des outils de migration dédiés. |

## Dépannage et FAQ

### Problèmes courants

1. **« Pilote non trouvé » / « Connexion impossible »**
   - DBeaver vous invitera à télécharger le pilote. Si le téléchargement automatique échoue, allez dans `Database → Driver Manager`, sélectionnez votre base de données et cliquez sur **Download/Update**.
   - Assurez-vous d'avoir un accès Internet ou placez manuellement le fichier JAR dans la bibliothèque de pilotes.

2. **La connexion se bloque ou expire**
   - Vérifiez la connectivité réseau et les règles du pare-feu.
   - Vérifiez les paramètres SSH/SSL ; un tunnel mal configuré peut bloquer les connexions.
   - Augmentez le délai d'expiration de la connexion dans les propriétés du pilote.

3. **Les performances du SQL Editor sont lentes**
   - Désactivez le chargement automatique des métadonnées : `Preferences → Database → Navigator → Disable lazy metadata reading`.
   - Réduisez la limite de l'ensemble de résultats dans la barre d'outils de l'éditeur.

4. **Impossible de modifier les BLOB/CLOB**
   - DBeaver prend en charge l'édition en ligne pour les petits objets. Pour les grands objets, utilisez la boîte de dialogue **View / Edit Value** (clic droit sur la cellule → **View Value**).

### Foire aux questions

**Q : DBeaver est-il entièrement gratuit ?**
**R :** La version Community est gratuite et open-source (Apache 2.0). Les éditions Pro, Enterprise et Team sont commerciales et ajoutent des fonctionnalités telles que la prise en charge NoSQL, l'assistance IA et une CLI.

**Q : Puis-je utiliser DBeaver pour des bases de données de production ?**
**R :** Oui, la version Community est prête pour la production pour les tâches de développement et d'administration de bases de données. Pour les environnements critiques, envisagez l'édition Enterprise avec un support et un audit supplémentaires.

**Q : DBeaver fonctionne‑t‑il avec MongoDB ou d'autres bases de données NoSQL ?**
**R :** La version Community prend en charge MongoDB de base. La prise en charge complète NoSQL et des bases de données cloud (y compris MongoDB, Cassandra et DynamoDB) est disponible dans l'édition Enterprise.

**Q : Comment désinstaller complètement DBeaver ?**
**R :** Utilisez le gestionnaire de paquets de votre système (par exemple, `brew uninstall --cask dbeaver-community`, `snap remove dbeaver-ce`) ou le désinstalleur du système d'exploitation. Les paramètres utilisateur sont stockés dans `~/.dbeaver` sur macOS/Linux ou `%APPDATA%\DBeaver` sur Windows ; supprimez ces répertoires pour effacer toute la configuration.

## Conclusion

DBeaver est un outil de base de données puissant, flexible et convivial qui s'intègre parfaitement dans le flux de travail de tout développeur. Son cœur open-source, sa prise en charge étendue des bases de données et son ensemble riche de fonctionnalités en font un utilitaire essentiel pour toute personne travaillant avec des données.

Pour plus d'informations, visitez la documentation officielle sur [dbeaver.com/docs](https://dbeaver.com/docs/) ou contribuez à la communauté sur [GitHub](https://github.com/dbeaver/dbeaver).