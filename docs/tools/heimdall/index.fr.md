---
title: Heimdall - Outil de flashage de firmware Samsung
description: Suite d'outils open-source multiplateforme pour flasher des firmware (ROMs) sur les appareils mobiles Samsung.
created: 2026-06-15
tags:
  - samsung
  - firmware
  - flashing
  - odin
  - android
  - open-source
status: draft
ecosystem: android
---

# Heimdall

## Qu'est-ce que Heimdall ?

Heimdall est une suite d'outils open-source multiplateforme conçue pour flasher des firmware (ROMs stock, ROMs personnalisées, bootloaders et images de recovery) sur les appareils Samsung Android. Il fonctionne directement via USB en utilisant le protocole propriétaire Odin de Samsung, fournissant une alternative gratuite et compatible Linux/macOS à l'outil Odin réservé à Windows. Le projet est maintenu sur GitHub par Benjamin Dobell et largement utilisé dans la communauté de modding Android depuis le début des années 2010.

## Pourquoi utiliser Heimdall ?

- **Multiplateforme** – Fonctionne nativement sous Windows, Linux et macOS sans émulation.
- **Open source** – Entièrement vérifiable et piloté par la communauté.
- **Contourne les restrictions d'Odin** – Utile quand Odin n'est pas disponible ou pour flasher sur des systèmes non Windows.
- **Scriptable** – L'interface en ligne de commande permet l'automatisation et l'intégration dans des chaînes d'outils personnalisées.
- **Flashage au niveau des partitions** – Flashez des images de partitions individuelles (par ex., `BOOT`, `SYSTEM`, `RECOVERY`) pour des modifications ciblées.

## Installation

### Windows
Téléchargez le dernier programme d'installation depuis la [page des versions GitHub](https://github.com/Benjamin-Dobell/Heimdall/releases). Lancez le `.exe` et suivez l'installateur graphique.

### Linux
Disponible via de nombreux gestionnaires de paquets :
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
Vous pouvez aussi compiler à partir des sources avec `cmake`.

### macOS
Installez via Homebrew :
```bash
brew install heimdall
```
Ou téléchargez le binaire macOS depuis la page des versions.

## Utilisation

### Prérequis
1. Activez les **options développeur** et le **débogage USB** sur l'appareil Samsung.
2. Démarrez l'appareil en **mode Download** (généralement : Éteindre → maintenir Volume Bas + Accueil + Marche/Arrêt, puis appuyer sur Volume Haut pour confirmer).
3. Connectez l'appareil à l'ordinateur via USB.

### Détection
Vérifiez que l'appareil est reconnu :
```bash
heimdall detect
```
En cas de succès, la sortie affiche le modèle de l'appareil et l'état de la connexion.

### Flashage de base
Flasher une image de partition :
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
Flasher plusieurs partitions à la fois :
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### Utilisation d'un fichier PIT
Pour une restauration complète du firmware ou lorsque la table de partitions est inconnue, fournissez un fichier `.pit` extrait de l'appareil ou du package de firmware :
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
Le drapeau `--SLT` flashe toutes les partitions définies dans le PIT, tandis que `--no-reboot` maintient l'appareil en mode Download après l'opération.

### Fermer la connexion
Après le flashage, fermez l'interface USB :
```bash
heimdall close-pc-screen
```

## Fonctionnalités clés

- **Multiplateforme** : Windows, Linux, macOS (binaires natifs).
- **Open source** : Code source sous licence BSD avec maintenance communautaire active.
- **Prise en charge du protocole Odin** : Implémentation directe du protocole de flashage bas niveau de Samsung.
- **Détection de l'appareil** : Énumération USB fiable et vérification de la poignée de main (handshake).
- **Flashage au niveau des partitions** : Flashez des partitions individuelles (boot, recovery, system, etc.).
- **Flashage basé sur PIT** : Utilisez les tables d'informations de partition pour une restauration complète du firmware.
- **Pilotes USB intégrés** : Les installateurs Windows incluent les pilotes nécessaires ; libusb est utilisé sur Linux/macOS.
- **Prise en charge des scripts** : Indicateurs CLI adaptés aux pipelines automatisés et aux environnements CI/CD.

## Exemples

### Détecter un appareil connecté
```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### Flasher une recovery personnalisée (TWRP)
```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### Flasher un firmware stock complet à l'aide d'un fichier PIT
```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### Flasher uniquement la partition boot
```bash
heimdall flash --BOOT boot.img
```

## Remarques

- Heimdall est distinct du **Heimdall Application Dashboard** (linuxserver/Heimdall, un lanceur d'applications web) et du framework de cybersécurité **Heimdall**.
- Utilisez toujours le firmware correct pour votre modèle d'appareil pour éviter de le briquer.
- Assurez-vous que les pilotes USB sont installés sous Windows – l'installateur les inclut. Sous Linux, des règles udev peuvent être nécessaires pour que l'appareil soit accessible sans root.