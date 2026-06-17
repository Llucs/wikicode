---
title: Module Magisk SpeedCool
description: Un module Magisk pour Android qui optimise les paramètres système pour booster les performances, réduire l'utilisation de la RAM et améliorer la gestion thermique.
created: 2026-06-15
tags:
  - android
  - magisk-module
  - performance-tuning
  - thermal-management
  - root
status: draft
ecosystem: android
---

# Module Magisk SpeedCool

**SpeedCool** est un module Magisk open-source et léger créé par [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module). Il applique automatiquement un ensemble complet de réglages au niveau du noyau et du système au démarrage pour booster les performances, réduire l'utilisation de la RAM et améliorer la gestion thermique sur tout appareil Android rooté.

Contrairement à un nettoyeur de bloatware standard, SpeedCool modifie la configuration sous-jacente du système pour éliminer les causes profondes du lag et de la surchauffe.

---

## Ce qu'il fait

SpeedCool cible plusieurs domaines clés du système :

- **Gouverneur CPU et scaling de fréquence :** Réduit la latence de réveil pour les applications exigeantes (ex. jeux, émulateurs).
- **Low Memory Killer (LMK) :** Priorise le maintien de l'application active en mémoire tout en récupérant agressivement la mémoire des processus de cache en arrière-plan.
- **Moteur thermique :** Modifie les points de throttling thermique pour équilibrer les performances soutenues avec la génération de chaleur.
- **Planificateur I/O :** Bascule le planificateur de stockage vers une variante à faible latence pour un chargement d'applications plus rapide.
- **Pile réseau :** Optimise le contrôle de congestion TCP pour un meilleur débit sur les réseaux mobiles.
- **Rendu GPU :** Active le rendu GPU forcé et optimise le gouverneur GPU.

---

## Pourquoi l'utiliser ?

- **Jeux plus fluides :** Les fréquences d'images sont plus stables grâce à un meilleur réglage du gouverneur CPU/GPU et un contrôle du throttling thermique.
- **Multitâche plus rapide :** Les applications se rechargent moins souvent grâce à des valeurs LMK optimisées.
- **Fonctionnement plus frais :** Des profils thermiques intelligents empêchent le SoC d'atteindre des températures critiques lors d'une utilisation intensive.
- **Optimiseur tout-en-un :** Remplace le besoin de multiples modules de performance conflictuels.
- **Léger :** Le module fait généralement moins de 1 Mo et a une surcharge négligeable.

---

## Installation

### Prérequis

- Appareil Android avec un bootloader déverrouillé et un accès root.
- **Magisk** (v20.0+) installé.
- Récupération personnalisée (TWRP) recommandée comme solution de secours.

### Étapes

1. **Téléchargez** le dernier `SpeedCool-Magisk-Module.zip` depuis la [page des versions GitHub](https://github.com/Llucs/SpeedCool-Magisk-Module/releases).
2. Ouvrez l'application **Magisk Manager**.
3. Accédez à l'onglet **Modules**.
4. Appuyez sur **Installer depuis le stockage**.
5. Sélectionnez le fichier `.zip` téléchargé.
6. Balayez pour confirmer l'installation.
7. **Redémarrez** votre appareil lorsque vous y êtes invité.

> **Astuce :** Si vous rencontrez un bootloop, démarrez en mode sans échec (maintenez Volume Haut au démarrage) et désactivez le module, ou supprimez-le manuellement via la récupération en supprimant `/data/adb/modules/SpeedCool/`.

---

## Utilisation et vérification

SpeedCool est conçu pour fonctionner entièrement en arrière-plan. Aucune interface utilisateur n'est requise. Vous pouvez vérifier son fonctionnement à l'aide de commandes terminal.

### Vérification de l'état actif

Listez le répertoire du module pour confirmer qu'il est installé :

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

S'il est monté avec succès, le répertoire contiendra les fichiers du module (`system.prop`, `service.sh`, `module.prop`).

### Vérification des propriétés système appliquées

```bash
su -c "getprop | grep speed"
```

Recherchez les propriétés injectées par le module (ex. `ro.sys.speedcool.version`).

---

## Fonctionnalités clés avec exemples de commandes

### 1. Gouverneur CPU
Le module force un gouverneur à faible latence (généralement `performance`, `interactive` ou `schedutil` modifié) sur tous les cœurs CPU.

```bash
# Vérifier le gouverneur actuel
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```
*Sortie attendue :* `performance` ou `schedutil`

### 2. Optimisation de la RAM (LMK)
Les seuils du Low Memory Killer sont modifiés pour garder l'application au premier plan réactive tout en tuant agressivement les processus d'arrière-plan moins utiles.

```bash
# Vérifier les valeurs LMK (adj, minfree)
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. Optimisation du planificateur I/O
Le planificateur de la couche bloc est basculé vers une variante optimisée pour les performances interactives (ex. `bfq` ou `fiops`).

```bash
# Vérifier le planificateur actif pour le périphérique de stockage principal
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```
*Sortie attendue :* `[bfq]` ou `[fiops]`

### 4. Réglages réseau
Le contrôle de congestion TCP est basculé vers un algorithme mieux adapté aux réseaux mobiles (ex. `westwood` ou `bbr`).

```bash
# Vérifier l'algorithme de congestion TCP actif
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```
*Sortie attendue :* `westwood`

### 5. Consultation des logs du module
Si le débogage est activé dans le script du module, vous pouvez filtrer le journal système.

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. Lecture du profil du module (si configurable)
Certaines versions vous permettent de choisir un profil en modifiant `service.sh`. Vérifiez les commentaires disponibles dans le fichier :

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| **Bootloop** | Module conflictuel ou appareil incompatible. | Maintenez Volume Haut au démarrage pour désactiver le module, ou supprimez le répertoire `/data/adb/modules/SpeedCool` dans le gestionnaire de fichiers de TWRP. |
| **Aucun changement de performance** | Modules conflictuels (LKT, FDE.AI, NFS). | Supprimez tous les autres modules de performance avant d'utiliser SpeedCool. |
| **Appareil toujours chaud** | Les limites thermiques sont trop agressives. | Vérifiez la configuration du thermal-engine dans le module ou essayez un autre profil. |
| **Applications qui plantent** | Valeurs LMK trop agressives. | Ajustez manuellement les valeurs `minfree` dans `service.sh`. |

---

## Suppression

1. Ouvrez **Magisk Manager**.
2. Allez dans l'onglet **Modules**.
3. Appuyez sur l'icône **Supprimer** (poubelle) à côté de SpeedCool.
4. Appuyez sur **Redémarrer**.

**Suppression alternative en ligne de commande :**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## Références

- **Dépôt GitHub :** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Documentation officielle de Magisk :** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers :** Recherchez *SpeedCool* ou *Llucs* pour les discussions de support communautaire.

> **Avertissement :** La modification des paramètres système comporte des risques inhérents. Effectuez toujours une sauvegarde Nandroid complète avant d'installer des modules de performance. Les auteurs ne sont pas responsables des dommages causés à votre appareil.