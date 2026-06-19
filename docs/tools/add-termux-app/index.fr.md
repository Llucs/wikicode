---
title: "Termux : Émulateur de terminal et environnement Linux pour Android"
description: "Un guide complet sur Termux, le puissant émulateur de terminal open-source et environnement Linux pour appareils Android, couvrant l'installation, la gestion des paquets, l'utilisation avancée et les workflows de développement."
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux : Émulateur de terminal et environnement Linux pour Android

## Qu'est-ce que Termux ?

Termux est un **émulateur de terminal et environnement Linux open-source** pour Android. Il fonctionne entièrement dans l'espace utilisateur, ne nécessitant **aucun accès root**, et fournit un riche dépôt de paquets dérivé de Debian/Ubuntu. Avec Termux, vous pouvez vivre une expérience complète de ligne de commande Linux sur votre appareil Android — installez des compilateurs, interpréteurs, éditeurs de texte, outils réseau, etc. Il exploite les appels système Linux du noyau Android pour créer un environnement quasi natif.

### Pourquoi utiliser Termux ?

- **Environnement de développement portable** – Écrivez et exécutez des scripts Python, compilez des programmes C, gérez des dépôts Git, ou utilisez un REPL directement sur votre téléphone.
- **Administration de serveur en déplacement** – Connectez-vous en SSH à des serveurs distants, vérifiez les diagnostics réseau (ping, traceroute, nmap), et synchronisez des fichiers avec rsync.
- **Apprentissage et éducation** – Pratiquez les commandes Linux, l'écriture de scripts shell et les concepts réseau sans avoir besoin d'un PC complet.
- **Automatisation et intégration** – Combinez avec des applications d'automatisation Android (Tasker) ou utilisez Termux:API pour interagir avec le matériel du téléphone (appareil photo, capteurs, presse-papiers).
- **Distributions Linux complètes** – Installez Ubuntu, Debian, Arch ou Fedora dans un environnement Termux en utilisant proot-distro pour presque toutes les tâches Linux.

---

## Fonctionnalités clés

| Fonctionnalité | Description |
|---------|-------------|
| **Émulateur de terminal** | Entièrement équipé avec des commandes gestuelles adaptées au tactile, des touches de fonction supplémentaires (Tab, Ctrl, Alt, Esc) accessibles en glissant vers la gauche depuis la rangée de chiffres. |
| **Gestionnaire de paquets** | `pkg` (et `apt` sous-jacent) avec des milliers de paquets provenant du dépôt Termux. |
| **Gestion multi-session** | Tirez un tiroir pour gérer des sessions de terminal séparées, chacune connectée indépendamment. |
| **Client et serveur SSH** | Connectez-vous à des serveurs distants avec `ssh`, ou démarrez un serveur (`sshd`) pour accéder à votre appareil depuis un ordinateur. |
| **Support des distributions Proot** | Exécutez des distributions Linux complètes (Ubuntu, Debian, Arch, Fedora) en utilisant `proot-distro`. |
| **Intégration d'API** | L'application compagne *Termux:API* donne aux scripts l'accès aux capteurs Android, au presse-papiers, à la synthèse vocale (TTS), à l'appareil photo, aux notifications, et plus. |
| **Accès au stockage** | Montez le stockage Android partagé (interne/SD) via `termux-setup-storage`. |

---

## Installation

### 1. Obtenir Termux

> **Important** : La **version du Google Play Store est dépréciée** (bloquée à l'API 28). Installez toujours depuis **F-Droid** pour des paquets à jour et une compatibilité totale avec Android moderne (10+).

- **Client F-Droid** : Recherchez « Termux » dans l'application F-Droid ou téléchargez l'APK directement depuis [F-Droid](https://f-droid.org/packages/com.termux/).
- **APK direct** : [F-Droid APK](https://f-droid.org/repo/com.termux_*.apk) (toujours la dernière version).

### 2. Applications compagnes (optionnelles mais recommandées)

| App | Objectif |
|-----|---------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | Accédez au matériel Android (capteurs, appareil photo, presse-papiers, etc.) depuis des scripts. |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | Exécutez Termux dans une fenêtre flottante (superposition). |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | Schémas de couleurs et polices compatibles Powerline pour le terminal. |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | Appelez des exécutables Termux depuis Tasker et les applications d'automatisation compatibles. |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | Lancez de petits scripts depuis l'écran d'accueil. |

### 3. Configuration initiale

Après avoir lancé Termux pour la première fois :

```bash
# Update the package repository and upgrade all packages
pkg update && pkg upgrade

# Grant storage access (needed to see your shared folders)
termux-setup-storage
```

Vous avez maintenant un environnement Termux entièrement mis à jour. Le stockage Android partagé est monté dans `~/storage/shared`.

---

## Gestion des paquets

Termux utilise la commande **`pkg`** comme interface autour de **`apt`**. Toutes les commandes sont familières aux utilisateurs de Debian/Ubuntu.

### Opérations courantes de gestion des paquets

```bash
# Search for a package
pkg search python

# Install packages
pkg install python git vim openssh curl wget

# Remove a package
pkg remove python2

# List installed packages
pkg list-installed

# Upgrade all packages
pkg upgrade
```

### Paquets disponibles (échantillon)

| Catégorie | Paquets |
|----------|----------|
| **Langages** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **Compilateurs/Outils** | clang, make, gdb, cmake, gcc (via proot distro) |
| **Éditeurs** | vim, emacs, nano, neovim |
| **Réseau** | openssh, nmap, traceroute, netcat, rclone |
| **Bases de données** | mariadb, sqlite, postgresql (requires proot) |
| **Utilitaires** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **Note** : Comme Termux est un environnement en espace utilisateur, certains paquets au niveau système (par ex., `systemd`, dépendances `glibc`) nécessitent une distribution Linux complète via `proot-distro`.

---

## Utilisation avancée

### 1. SSH : Client et serveur

**Client** – Connectez-vous à des machines distantes comme sur un ordinateur de bureau :

```bash
pkg install openssh
ssh user@hostname
```

**Serveur** – Rendez votre appareil Android accessible via SSH (port par défaut 8022) :

```bash
sshd
# or start it in the foreground with -d
sshd -d
```

Connectez-vous depuis une autre machine :

```sh
ssh user@phone-ip -p 8022
```

La première fois que vous exécutez `sshd`, Termux générera des clés d'hôte et vous pourrez définir un mot de passe pour l'utilisateur termux (l'utilisateur par défaut est `u0_aXYZ`). Utilisez `passwd` pour le changer.

### 2. Exécuter des distributions Linux complètes avec `proot-distro`

Proot vous permet d'exécuter une distribution Linux standard dans Termux sans root. Le paquet `proot-distro` simplifie cela.

```bash
pkg install proot-distro

# List available distributions
proot-distro list

# Install Ubuntu (example)
proot-distro install ubuntu

# Login to the installed distribution
proot-distro login ubuntu

# Within the Ubuntu environment, you can use apt normally.
```

Vous avez maintenant un environnement Ubuntu complet (y compris des gestionnaires de services de type `systemd` via `proot`, bien que toutes les fonctionnalités ne fonctionnent pas parfaitement). Vous pouvez installer des paquets comme `gcc`, `postgresql` ou `firefox` (l'interface graphique nécessite un serveur X) à l'intérieur.

### 3. Utiliser l'application compagne Termux:API

Avec `Termux:API` installé, vous pouvez contrôler les fonctionnalités Android depuis la ligne de commande.

```bash
pkg install termux-api

# Get battery status
termux-battery-status

# Take a photo
termux-camera-photo output.jpg

# Get clipboard content
termux-clipboard-get

# Show a notification
termux-notification --title "Hello" --content "World"

# Check sensors
termux-sensor -s "Accelerometer" -n 5
```

### 4. Automatisation avec Tasker

Termux:Tasker vous permet d'exécuter des scripts Termux comme des actions Tasker.

1. Installez **Termux:Tasker** depuis F-Droid.
2. Dans Tasker, ajoutez une action de type `System -> Send Intent`.
3. Action : `com.termux.tasker.RUN_COMMAND`
4. Paires clé/valeur supplémentaires : `command` = votre script ou commande (par ex., `termux-battery-status`).

Vous pouvez également placer des scripts dans `~/.termux/tasker/` et les appeler par leur nom.

### 5. Gestion des sessions et astuces d'interface

- **Touches supplémentaires** : Glissez vers la gauche depuis la rangée de chiffres (en haut du clavier) pour révéler une rangée avec Tab, Ctrl, Alt, Esc, un basculement de touche Fonction et une flèche vers le haut (pour faire défiler). Vous pouvez les personnaliser dans `~/.termux/termux.properties`.
- **Multi-session** : Appuyez sur l'icône du tiroir (trois lignes horizontales) sur le côté gauche de l'écran pour lister, changer ou créer de nouvelles sessions de terminal.
- **Sélection de texte** : Appuyez longuement dans la zone du terminal pour entrer en mode sélection ; copier/coller fonctionne avec le menu de débordement.

---

## Cas d'utilisation

- **Codage mobile** – Écrivez et testez des scripts Python, des applications Node.js ou des programmes C avec vim et gcc. Utilisez git pour le contrôle de version.
- **Opérations serveur** – Connectez-vous en SSH à des serveurs de production, exécutez des analyses `tcpdump` ou `nmap`, surveillez les journaux et transférez des fichiers avec `rsync`.
- **Analyse de données** – Installez Python avec pandas, numpy, scipy et Jupyter (via `pkg install jupyter`) pour le traitement de données en déplacement.
- **Apprentissage de Linux** – Expérimentez avec le système de fichiers, les scripts shell et le réseau sans PC séparé.
- **Calculatrice de poche** – Utilisez Python comme calculatrice interactive : `python -c 'print(2**100)'` ou lancez un REPL.

---

## Dépannage et conseils

### L'installation d'un paquet échoue avec « 404 Not Found »

Les dépôts sont peut-être obsolètes. Exécutez d'abord `pkg update && pkg upgrade`. Si le problème persiste, vérifiez que vous utilisez la version F-Droid (pas Google Play).

### Accès au stockage refusé

Exécutez `termux-setup-storage` et accordez l'autorisation lorsque vous y êtes invité. Si cela échoue sur Android 11+, assurez-vous que Termux a l'autorisation « Fichiers et médias » activée dans les paramètres système.

### Problèmes avec les dépendances libc/glibc

Certains paquets s'attendent à glibc, mais Termux utilise bionic (libc d'Android). Utilisez une proot-distro (Ubuntu, Debian) pour ces paquets.

### Comment désactiver le clavier plein écran sur Android 10+

Ajoutez cette ligne à `~/.termux/termux.properties` :
```
fullscreen=false
```
Puis rechargez avec `termux-reload-settings`.

### Intégration du presse-papiers avec le terminal

Utilisez `termux-clipboard-get` et `termux-clipboard-set` de `termux-api` pour interagir avec le presse-papiers système.

---

## Communauté et ressources

- **Site officiel** : [termux.com](https://termux.com) (redirige vers GitHub)
- **Dépôt GitHub** : [termux/termux-app](https://github.com/termux/termux-app) (application principale)
- **Dépôt de paquets** : [termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki** : [Termux Wiki](https://wiki.termux.com)
- **F-Droid** : [F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit** : [r/termux](https://reddit.com/r/termux)

---

Termux transforme votre appareil Android en un puissant poste de travail Linux portable. Avec son vaste dépôt de paquets, ses capacités SSH et sa compatibilité avec les workflows Linux standard, c'est un outil indispensable pour les développeurs, les administrateurs système et tous ceux qui aiment garder la ligne de commande dans leur poche.