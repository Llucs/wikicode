---
title: Magisk - Root système sans modification et gestionnaire de modules pour Android
description: Magisk est un outil de root Android populaire qui offre un accès root sans modification système et un support de modules pour les modifications système.
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Root système sans modification et gestionnaire de modules pour Android

## Qu'est-ce que Magisk ?

Magisk est une suite logicielle open-source créée par **John Wu (topjohnwu)** qui permet un **root sans modification système** et une personnalisation approfondie des appareils Android. Contrairement aux méthodes de root traditionnelles qui modifient la partition `/system` immuable, Magisk fonctionne en patchant l'image de démarrage de l'appareil (ou la partition `init_boot` sur les appareils plus récents) pour créer un système de fichiers superposé au moment du démarrage. Cela permet un accès root, des scripts de démarrage, des correctifs de politique SELinux et des modules de charger **sans altérer de manière permanente les fichiers système**.

Initialement publié en 2016, Magisk est rapidement devenu la solution de root Android standard, remplaçant des outils plus anciens comme SuperSU. Il continue d'être activement maintenu et est largement utilisé pour le root de base ainsi que pour les modifications avancées des appareils.

---

## Pourquoi utiliser Magisk ?

| Bénéfice | Description |
|---------|-------------|
| **Modifications sans système** | Les mises à jour OTA sont conservées car `/system` reste intact. |
| **MagiskSU** | Gestion des permissions root open-source pure (accorder, demander, refuser). |
| **Système de modules** | Installer des modifications (mods audio, bibliothèques caméra, blocage de publicités, polices) sans repartitionnement. |
| **Zygisk** | Injection de code dans chaque processus d'application via Zygote – remplace MagiskHide. |
| **DenyList** | Masquer le root, les modules et le bootloader déverrouillé à des applications spécifiques (banque, streaming). |
| **MagiskBoot** | Outil puissant pour décompresser, modifier et recompacter les images de démarrage Android. |
| **Communauté active** | Des milliers de modules et une documentation complète disponibles. |

Magisk est essentiel pour les utilisateurs qui ont besoin d'un accès root pour des outils de sauvegarde avancés, l'automatisation (Tasker), des réglages système personnalisés, ou pour réactiver des fonctionnalités dans les applications qui bloquent les appareils rootés.

---

## Guide d'installation

### Prérequis

- **Bootloader déverrouillé** (spécifique à l'appareil, nécessite souvent un déverrouillage OEM).
- **ADB et Fastboot fonctionnels** sur votre ordinateur.
- **Image d'usine de l'appareil** ou `boot.img` d'origine (et éventuellement `init_boot.img`).
- **Sauvegardez** toutes les données importantes.

### Étape 1 – Extraire l'image de démarrage

Obtenez l'image d'usine pour votre appareil (par exemple, depuis la page des images d'usine de Google) et extrayez l'image de démarrage.

```bash
# Example for a Pixel device
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.img is now in the current directory
```

Pour les appareils fonctionnant sous Android 13+ (par exemple, la série Pixel 6), la partition root est `init_boot.img` au lieu de `boot.img`.

### Étape 2 – Patching de l'image avec l'application Magisk

1. Installez le dernier APK Magisk sur votre appareil.
2. Ouvrez l'application Magisk, appuyez sur **Installer** → **Sélectionner et patcher un fichier**.
3. Choisissez le fichier `boot.img` extrait (ou `init_boot.img`).
4. L'application va patcher l'image et sauvegarder un nouveau fichier nommé `magisk_patched-XXXXX.img` (généralement dans `Download/`).

### Étape 3 – Flasher l'image patchée

Transférez l'image patchée sur votre ordinateur, puis démarrez votre appareil en mode fastboot.

```bash
adb pull /storage/emulated/0/Download/magisk_patched-XXXXX.img .
adb reboot bootloader
# For most devices:
fastboot flash boot magisk_patched-XXXXX.img
# For Pixel 6+ (init_boot partition):
fastboot flash init_boot magisk_patched-XXXXX.img
# Reboot:
fastboot reboot
```

### Étape 4 – Vérifier l'installation

Après le redémarrage, ouvrez l'application Magisk. L'écran **Accueil** devrait afficher la version installée de Magisk et « Installé » à côté du statut Magisk.

---

## Utilisation de base

### Interface de l'application Magisk

- **Onglet Superuser** (icône de bouclier) : Liste toutes les applications qui ont demandé des permissions root. Appuyez sur une entrée pour modifier son statut de permission (Accorder / Demander / Refuser).
- **Onglet Modules** (icône de pièce de puzzle) : Affiche les modules installés. Appuyez sur le bouton **+** pour installer un nouveau module à partir d'un fichier `.zip` stocké sur votre appareil. Utilisez l'interrupteur pour activer/désactiver un module (la plupart nécessitent un redémarrage).
- **Onglet Paramètres** (icône d'engrenage) :
  - **Zygisk** : Activer ou désactiver Zygisk (nécessite un redémarrage).
  - **DenyList** : Configurer les applications auxquelles Magisk doit se cacher (nécessite Zygisk et un redémarrage).
  - **Canal de mise à jour** : Choisir Stable, Beta ou Canary pour les mises à jour de l'application et de Magisk.
  - **Réponse automatique** : Définir le comportement par défaut des permissions root.

### Gestion des modules

Les modules sont installés sous forme d'archives ZIP standard. Ils peuvent contenir des scripts simples, des fichiers binaires ou des répertoires de superposition système complets.

```bash
# Typical module ZIP structure (inside /data/adb/modules/<module_id>/)
module.prop          # Metadata (id, name, version, author)
system/              # Files to overlay on /system
post-fs-data.sh      # Script run early in boot
service.sh           # Script run later in boot
```

Pour installer un module manuellement :

1. Téléchargez le fichier `.zip` du module sur votre appareil.
2. Ouvrez l'application Magisk → onglet Modules → **Installer depuis le stockage**.
3. Sélectionnez le fichier, confirmez, puis **Redémarrez** lorsque vous y êtes invité.

### Désinstallation de Magisk

L'application Magisk offre un moyen direct de supprimer complètement le root :

1. Ouvrez l'application Magisk.
2. Appuyez sur **Désinstaller Magisk** en bas de l'écran d'accueil.
3. Confirmez – l'application restaurera l'image de démarrage originale non patchée et redémarrera.

---

## Fonctionnalités clés

### MagiskSU

Un remplacement complet de `su` entièrement open-source. Il implémente un modèle de permissions avec les options Accorder / Demander / Refuser et enregistre tous les accès root. MagiskSU est compatible avec toutes les applications existantes nécessitant root.

### Magisk Modules

Un format standardisé pour distribuer des modifications système sans toucher à la partition système. Les modules sont chargés au démarrage en utilisant le système de fichiers superposé de Magisk. Des milliers de modules existent sur des forums comme XDA et le dépôt Magisk.

### Zygisk

Zygisk est l'implémentation par Magisk de l'injection de code dans le processus Zygote. Il permet des modifications à l'exécution à l'intérieur de n'importe quel processus d'application. Zygisk remplace l'ancienne fonctionnalité MagiskHide.

### DenyList

Lorsque Zygisk est activé, vous pouvez configurer une **DenyList** d'applications où Magisk cache sa présence (root, modules, bootloader déverrouillé). C'est la méthode moderne pour contourner les vérifications d'intégrité utilisées par les applications bancaires, de paiement et de streaming.

### MagiskBoot

MagiskBoot est un outil de bas niveau pour travailler avec les images de démarrage. Il peut les décompresser, les modifier et les recompacter sans nécessiter un environnement Android complet. Il est souvent utilisé directement sur un ordinateur pour créer des images patchées sans l'application.

---

## Exemples de commandes

### Flasher une image de démarrage patchée (fastboot)

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### Flasher init_boot pour les appareils plus récents

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### Utiliser MagiskBoot pour décompresser une image de démarrage

```bash
magiskboot unpack boot.img
# This creates: kernel, kernel_dtb, ramdisk.cpio, header, etc.
```

### Recompacter une image de démarrage modifiée avec MagiskBoot

```bash
magiskboot repack boot.img
# Creates new-boot.img with your modifications.
```

### Vérifier l'en-tête de l'image de démarrage

```bash
magiskboot info boot.img
```

### Patcher une image de démarrage avec Magisk (ligne de commande)

Si vous avez l'exécutable Magisk sur votre ordinateur, vous pouvez patcher directement :

```bash
magiskboot boot.img
# Creates patched_boot.img in the current directory.
```

### Cacher Magisk à une application (DenyList)

Ouvrez l'application Magisk → Paramètres → **Configurer DenyList** → ajoutez l'application cible (par exemple, `com.google.android.gms` pour Google Play Services). Après un redémarrage, Magisk sera invisible pour cette application.

---

## Conseils et considérations

- **Mises à jour OTA** restent compatibles car Magisk ne modifie que la partition de démarrage. Cependant, après une OTA, vous devez **re-flasher Magisk** sur la nouvelle image de démarrage.
- **SafetyNet / Play Integrity** – Bien que Magisk lui-même ne fournisse pas de contournement d'intégrité, des outils comme les modules Zygisk-Assistant ou Shamiko peuvent aider à cacher le root aux vérifications d'attestation de Google.
- **Conflits de modules** – Certains modules peuvent interférer entre eux ; désactivez-les un par un pour isoler les problèmes.
- **Sauvegardes** – Gardez toujours une copie de l'image de démarrage d'origine. Si quelque chose tourne mal, vous pouvez la restaurer via fastboot.
- **Magisk Canary** – Le canal de pointe inclut parfois des fonctionnalités instables. Utilisez-le uniquement pour les tests.

---

## Références

- [Dépôt GitHub de Magisk](https://github.com/topjohnwu/Magisk)
- [Documentation officielle de Magisk (guides développeur)](https://topjohnwu.github.io/Magisk/)
- [Dépôt de modules Magisk (non officiel)](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Discussion et support Magisk](https://forum.xda-developers.com/f/magisk.5903/)

---

*Ce document fait partie du wiki développeur. Les commentaires et améliorations sont les bienvenus.*