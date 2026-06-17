---
title: Team Win Recovery Project (TWRP)
description: TWRP est une recovery personnalisée open-source pour Android qui permet de flasher des ROMs personnalisées, d'effectuer des sauvegardes complètes de l'appareil (NANDroid) et de réaliser des modifications système via une interface tactile.
created: 2026-06-17
tags:
  - android
  - recovery
  - custom-rom
  - backup
  - twrp
status: draft
---

# Team Win Recovery Project (TWRP)

TWRP (Team Win Recovery Project) est une **image de recovery personnalisée open-source** pour les appareils Android. Elle remplace la partition de recovery d'origine pour fournir un environnement riche en fonctionnalités, piloté par écran tactile, permettant d'installer des firmwares tiers, de créer des sauvegardes système complètes et d'effectuer des tâches avancées de gestion système — le tout sans avoir à démarrer sur Android.

## Pourquoi TWRP ?

La recovery Android d'origine est limitée aux réinitialisations d'usine et aux mises à jour OTA. TWRP ouvre l'appareil pour :

- **Installation de ROMs personnalisées** (LineageOS, Pixel Experience, etc.)
- **Sauvegardes et restaurations système complètes** (NANDroid) — essentielles avant des modifications risquées.
- **Rooting** (flashage de Magisk ou SuperSU).
- **Gestion des partitions** (effacement, formatage, redimensionnement).
- **Gestion du chiffrement** (déchiffrement des userdata dans certaines conditions).
- **ADB sideload et MTP** pour transférer des fichiers ou flasher sans stockage.

TWRP est le standard de facto pour les passionnés et développeurs Android ; il a remplacé les recoveries antérieures comme ClockworkMod (CWM) grâce à son interface intuitive et au soutien actif de la communauté.

## Principales fonctionnalités

- **Interface graphique tactile (GUI)** – Prise en charge complète du tactile avec clavier à l'écran, gestionnaire de fichiers et émulateur de terminal.
- **Sauvegarde NANDroid** – Clone les partitions entières (Boot, System, Data, EFS/IMEI) vers `/sdcard/TWRP/BACKUPS/`.
- **Flashage ZIP** – Installe des packages de firmware personnalisés (ROMs, noyaux, mods, GApps, Magisk).
- **Effacement avancé** – Efface des partitions individuelles, « Format Data » pour supprimer le chiffrement.
- **Gestionnaire de fichiers** – Parcourir et modifier les fichiers sur le système de fichiers de l'appareil.
- **ADB Sideload** – Flasher des fichiers ZIP depuis un ordinateur via USB.
- **Support MTP** – Accéder au stockage de l'appareil comme un disque amovible dans la recovery.
- **Support du chiffrement** – Peut déchiffrer les userdata avec code PIN/mot de passe/motif (anciens chiffrements ; FBE sur les appareils modernes est souvent non supporté).
- **Personnalisation (Theming)** – Interface personnalisable via des thèmes `.twres`.
- **Capture d'écran** – Capturer l'écran dans la recovery.

## Historique

Créé par *Dees_Troy* vers 2011, TWRP est rapidement devenu la recovery personnalisée la plus populaire grâce à son interface tactile propriétaire. Elle a évolué d'un thème Holo à une interface Material Design (version 3.0+). Aujourd'hui, elle est maintenue par une équipe centrale et prend en charge des centaines d'appareils officiellement répertoriés sur [twrp.me](https://twrp.me).

## Installation

> **Prérequis :**
> - Bootloader déverrouillé (nécessaire pour la plupart des appareils).
> - Outils ADB & Fastboot installés sur votre PC.
> - Image TWRP correcte pour le modèle exact de votre appareil (vérifiez le nom de code sur twrp.me).

### Méthode Fastboot générale (la plupart des appareils)

1. **Redémarrer en mode bootloader :**
   ```bash
   adb reboot bootloader
   ```
2. **Flasher l'image de recovery :**
   ```bash
   fastboot flash recovery twrp-<version>.img
   ```
3. **Démarrer immédiatement sur la recovery** (avant que le système ne démarre, ce qui pourrait écraser TWRP) :
   ```bash
   fastboot reboot recovery
   # ou utiliser la combinaison de touches matérielles (Vol Up + Power, etc.)
   ```

### Appareils à fentes (partitions A/B – ex. : Pixels, OnePlus)

Étant donné que le système peut automatiquement remplacer la partition de recovery au prochain démarrage, utilisez une méthode de démarrage temporaire :

1. **Démarrer temporairement l'image TWRP :**
   ```bash
   fastboot boot twrp-<version>.img
   ```
2. **Dans TWRP, allez dans** *Advanced → Install Recovery Ramdisk*.
   - Ceci flashe TWRP sur la fente inactive et l'empêche d'être écrasé.

### Appareils Samsung (via Odin)

1. Téléchargez le fichier `.tar` TWRP (généralement nommé `twrp-<version>-<device>.tar`).
2. Ouvrez Odin, placez le fichier dans la fente **AP**.
3. Décochez **Auto-Reboot** dans les options d'Odin.
4. Flashez, puis redémarrez immédiatement sur la recovery en utilisant la combinaison de touches (Vol Up + Home + Power) pour empêcher la restauration de la recovery d'origine.

### Depuis un appareil rooté (en utilisant l'application TWRP officielle)

1. Installez l'**application TWRP officielle** depuis le Play Store ou twrp.me.
2. Accordez les permissions root.
3. Sélectionnez votre appareil et flashez la dernière image.

### Depuis le terminal (rooté)

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

Remplacez le chemin par l'emplacement de votre partition de recovery (varie selon l'appareil – trouvez avec `parted` ou `ls /dev/block/platform/...`).

## Flux de travail d'utilisation de base

### Entrer en recovery
- Utilisez la combinaison de touches matérielles (varie selon le fabricant, souvent **Volume Down + Power**).
- Ou depuis Android (si rooté/bootloader déverrouillé) : `adb reboot recovery`.

### Effacement des partitions

- **Factory Reset** (effacement des data/cache) – requis avant d'installer une nouvelle ROM.
  - *Wipe → Swipe to Factory Reset*
- **Format Data** – supprime le chiffrement et efface le stockage interne.
  - *Wipe → Format Data → tapez “yes”*.
- **Advanced Wipe** – sélectionnez les partitions individuelles à effacer.

### Installation d'un ZIP (ROM, GApps, Magisk, etc.)

1. Appuyez sur **Install**.
2. Naviguez vers le fichier `.zip` (généralement sur `/sdcard` ou SD externe).
3. Appuyez sur le fichier ; éventuellement appuyez sur **Add more Zips** pour mettre plusieurs fichiers en file d'attente.
4. **Swipe to Confirm Flash**.
5. *(Facultatif)* Redémarrez le système.

> Exemple de commande pour le sideload :
> ```bash
> adb sideload custom_rom.zip
> ```

### Sauvegarde (NANDroid)

1. Appuyez sur **Backup**.
2. Sélectionnez les partitions :
   - **Boot**, **System**, **Data** (minimum pour une restauration système complète).
   - **EFS** (stocke l'IMEI – critique pour certains appareils).
3. Balayez pour commencer la sauvegarde.
4. La sauvegarde est stockée dans `/sdcard/TWRP/BACKUPS/<device_serial>/`.

### Restauration d'une sauvegarde

1. Appuyez sur **Restore**.
2. Sélectionnez une sauvegarde dans la liste.
3. Cochez les partitions que vous souhaitez restaurer.
4. Balayez pour confirmer.

### Gestionnaire de fichiers et terminal

- **File Manager** : *Advanced → File Manager* – naviguer, supprimer, renommer, copier des fichiers.
- **Terminal** : *Advanced → Terminal* – exécuter des commandes en tant que root.

## Exemples de commandes (Fastboot et ADB)

```bash
# Reboot to bootloader from Android
adb reboot bootloader

# Flash recovery
fastboot flash recovery twrp-3.7.1_12-0-beryllium.img

# Boot into recovery without flashing
fastboot boot twrp-3.7.1_12-0-beryllium.img

# Sideload a file from PC
adb sideload LineageOS-21.0-20260617-UNOFFICIAL-beryllium.zip

# Push a file to the device in MTP mode
adb push magisk.zip /sdcard/
```

## Avertissements importants

- **Images spécifiques à l'appareil** – Flasher une image TWRP pour un modèle différent peut **hard brick** votre appareil. Vérifiez toujours le nom de code (par ex., `beryllium` pour Pocophone F1).
- **Confusion des fentes A/B** – Sur les appareils avec mises à jour transparentes, TWRP doit être installé sur les deux fentes. Si une fente n'a pas TWRP, l'appareil peut revenir à la recovery d'origine.
- **Problèmes de chiffrement** – Android moderne utilise le **File‑Based Encryption (FBE)**. TWRP ne peut souvent pas déchiffrer les userdata. Les utilisateurs doivent souvent **Format Data** (efface le stockage interne) lorsqu'ils changent de ROM ou si TWRP ne peut pas monter `/data`.
- **OTA avec recovery personnalisée** – Les mises à jour OTA officielles échouent généralement avec TWRP. Vous devez soit :
  - Flasher le ZIP OTA manuellement via TWRP.
  - Ou revenir à la recovery d'origine avant d'appliquer l'OTA.
- **Play Integrity / applications bancaires** – Un bootloader déverrouillé (requis pour TWRP) casse de nombreux contrôles de sécurité. Rooter avec Magisk peut le cacher, mais ajoute de la complexité et n'est pas toujours réussi.
- **Sauvegarder avant de modifier** – Créez toujours une sauvegarde NANDroid avant de flasher une nouvelle ROM ou un mod risqué. Une sauvegarde complète peut sauver d'un soft brick en quelques minutes.

## Dépannage

| Problème | Solution |
|--------|----------|
| TWRP ne persiste pas après redémarrage | Utilisez `fastboot boot` puis « Install Recovery Ramdisk » (appareils A/B). Autre option : reflasher et démarrer immédiatement sur la recovery. |
| Impossible de monter `/data` | Probablement chiffré. Allez dans *Wipe → Format Data* et tapez « yes ». **Cela efface tout le stockage interne.** |
| L'appareil reste sur le logo de démarrage après flash | Essayez d'effacer le cache Dalvik/ART et le Cache. Si cela échoue encore, restaurez une sauvegarde précédente. |
| ADB Sideload bloqué à « sending » | Assurez-vous d'avoir les derniers pilotes ADB. Essayez un autre câble/port USB. |
| TWRP ne démarre pas (écran noir) | L'image est peut-être corrompue ou incorrecte. Téléchargez-la à nouveau depuis le site officiel. |

## Ressources supplémentaires

- **Site officiel et téléchargements :** [https://twrp.me](https://twrp.me)
- **Code source :** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **Forums XDA :** Recherchez le fil de discussion spécifique à votre appareil pour les builds et le support TWRP.
- **Compilation de TWRP à partir des sources :** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

TWRP est un outil puissant pour tout développeur ou passionné Android. Utilisez-le avec sagesse et gardez toujours une sauvegarde à portée de main.