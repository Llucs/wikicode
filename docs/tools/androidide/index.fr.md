---
title: AndroidIDE - IDE de développement d'applications mobiles
description: Un guide complet d'AndroidIDE, l'IDE open-source pour développer des applications Android directement sur des appareils Android.
created: 2026-06-25
tags:
  - android-ide
  - mobile-development
  - gradle
  - open-source
  - android-sdk
  - java
  - kotlin
status: draft
---

# AndroidIDE – Créez des applications Android sur Android

AndroidIDE est un **environnement de développement intégré (IDE) open-source** conçu pour fonctionner nativement sur les appareils Android, vous permettant de développer des applications Android complètes en utilisant Gradle, un éditeur de code intelligent et un terminal — le tout sur votre téléphone ou tablette. C'est une alternative complète à un flux de travail de bureau Android Studio, apportant l'intégralité du SDK Android, des outils de build et de l'expérience d'édition de code sur mobile.

---

## Qu'est-ce qu'AndroidIDE ?

AndroidIDE transforme votre appareil Android en un poste de développement portable. Il prend en charge :

- **Builds complets basés sur Gradle** – compilez, empaquetez et signez des APK et Android App Bundles (AAB) directement sur l'appareil.
- **Un éditeur de code intelligent** – coloration syntaxique, auto-complétion, détection d'erreurs et refactorisation pour Java, Kotlin et XML.
- **Outils intégrés** – visionneuse Logcat, terminal Linux (via Termux), explorateur de fichiers, support Git et signataire APK.
- **Compatibilité des projets** – importez et travaillez avec des projets Android Studio standard (Gradle wrapper, build.gradle.kts/module, etc.).

AndroidIDE est construit sur une architecture moderne qui sépare le frontend IDE des processus de build/backend, le rendant à la fois puissant et optimisé pour mobile. Il est particulièrement utile pour les étudiants, les amateurs ou tout développeur souhaitant apprendre ou prototyper des applications Android sans accès à un PC de bureau.

---

## Fonctionnalités clés

- **Wrapper Gradle complet** – utilisez les mêmes scripts `gradlew` que sur un bureau, avec prise en charge de toutes les tâches Gradle standard.
- **Éditeur de code multi-langage** – Java, Kotlin, XML avec coloration syntaxique sémantique, complétion de code et indicateurs d'erreur en ligne.
- **Synchronisation de projet** – télécharge automatiquement les dépendances, les plates-formes SDK et les outils de build.
- **Génération APK / AAB** – builds debug et release, signés avec votre propre keystore.
- **Terminal intégré** – un environnement Linux réel (Termux) pour des commandes personnalisées comme `adb`, `git` ou `./gradlew ...`.
- **Visionneuse Logcat** – sortie de log en direct de l'application pour déboguer votre application en temps réel.
- **Intégration Git** – opérations de contrôle de version de base (commit, push, pull) depuis l'IDE.
- **Gestionnaire de fichiers** – parcourez, renommez, supprimez facilement les fichiers du projet.
- **Conscient de l'appareil** – détecte automatiquement le JDK, le SDK Android, le NDK et CMake installés ; exécute les builds en utilisant le CPU de l'appareil.

---

## Pourquoi utiliser AndroidIDE ?

- **Démocratise le développement** – n'importe qui avec un appareil Android peut commencer à créer des applications sans posséder de PC.
- **Débogage en déplacement** – testez et corrigez rapidement les problèmes sans retourner à un bureau.
- **Outil éducatif** – idéal pour enseigner le développement Android dans les régions où les PC sont rares.
- **Prototypage rapide** – esquissez une idée et exécutez-la immédiatement sur le même appareil.
- **100 % open source** – sous licence GPL-3.0, activement maintenu sur GitHub.

---

## Installation

### Prérequis

- **Android 7.0 (API 24)** ou supérieur
- Minimum **4 Go de RAM** (8 Go recommandé)
- Au moins **3 Go d'espace libre** (plus si vous travaillez sur plusieurs projets)
- Un SoC relativement moderne (Snapdragon 8xx, MediaTek Dimensity ou équivalent)

### Étapes

1. **Téléchargez l'APK** – obtenez la dernière version depuis la [page des versions officielles GitHub](https://github.com/AndroidIDE/AndroidIDE/releases).  
   (L'APK est également disponible sur F-Droid pour la v2.7.1‑bêta et ultérieures.)

2. **Autorisez l'installation à partir de sources inconnues** – dans les Paramètres de votre appareil → Sécurité → activez « Installer à partir de sources inconnues » pour votre gestionnaire de fichiers ou navigateur.

3. **Installez l'APK** – ouvrez le fichier téléchargé et procédez à l'installation.

4. **Premier lancement** – accordez l'autorisation de stockage lorsque vous y êtes invité. AndroidIDE téléchargera et configurera automatiquement :
   - OpenJDK 17
   - Android SDK (platform tools, build tools, plateforme pour le dernier SDK)
   - Distribution Gradle

   Cette configuration initiale peut prendre **20 à 30 minutes** en fonction de la vitesse de votre connexion Internet et des performances de votre appareil.

### Vérification de l'installation

Une fois la configuration terminée, vous pouvez vérifier les composants installés dans l'application :

- **Paramètres → Gestionnaire SDK** – affiche les plates-formes SDK, les outils de build et le NDK installés.
- **Terminal** – lancez le terminal intégré et exécutez :
  ```bash
  java -version
  gradle --version
  ```
  pour confirmer que le JDK et Gradle sont correctement configurés.

---

## Utilisation de base

### Créer un nouveau projet

1. Ouvrez AndroidIDE et appuyez sur **Nouveau projet** sur l'écran d'accueil.
2. Choisissez un modèle : **Activité vide** (Java ou Kotlin).
3. Spécifiez :
   - **Nom du projet**
   - **Nom du package** (ex : `com.example.myapp`)
   - **SDK minimum** (ex : API 24)
   - **Langage** (Java ou Kotlin)
4. Appuyez sur **Terminer**. L'IDE créera le projet (y compris le wrapper Gradle, les scripts de build et les fichiers sources par défaut).

### Écrire du code

L'éditeur d'AndroidIDE fournit :

- **Coloration syntaxique** pour Java, Kotlin, XML, etc.
- **Auto-complétion** pour les classes, méthodes, variables et ressources.
- **Détection d'erreurs en temps réel** – soulignements rouges pour les erreurs de compilation.
- **Actions rapides** – importer des classes, renommer des symboles, extraire des méthodes (refactorisation).

Ouvrez `MainActivity.java` ou `MainActivity.kt` depuis la vue du projet et commencez à coder.

### Compiler et exécuter

Il existe deux façons de compiler et d'exécuter votre application :

#### 1. Utiliser le bouton **Exécuter** (▶️)
- Cela invoque la tâche Gradle `assembleDebug`.
- Une fois l'APK compilé, AndroidIDE l'installe directement sur l'appareil (aucun câble ADB nécessaire).
- Si un émulateur est disponible (ou un deuxième appareil), vous pouvez choisir la cible.

#### 2. Via le **Terminal**
Ouvrez le terminal intégré (raccourci : `Ctrl+T` ou depuis le menu) et exécutez :
```bash
./gradlew assembleDebug
```
L'APK résultant se trouvera dans `app/build/outputs/apk/debug/app-debug.apk`. Vous pouvez l'installer manuellement :
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```
(ADB est préconfiguré et disponible dans le terminal.)

### Déboguer avec Logcat

- Appuyez sur l'icône **Logcat** (ou sélectionnez **Affichage → Logcat**).
- Filtrez par le nom du package de votre application.
- Consultez les traces de crash et les messages de débogage en temps réel pendant que votre application s'exécute.

### Utiliser le terminal

Le terminal est un environnement Linux complet (Termux). Vous pouvez :

- Exécuter des tâches `./gradlew` comme `clean`, `test`, `lint`, `assembleRelease`.
- Utiliser les commandes `git` : `git add .`, `git commit -m "message"`, `git push origin main`.
- Installer des outils supplémentaires : `pkg install tree` ou `apt update`.
- Accéder au stockage de l'appareil sous `/storage/emulated/0/`.

### Intégration Git

AndroidIDE inclut une boîte de dialogue **Git Commit** (accessible depuis le menu **VCS**) pour préparer, commiter et pousser les modifications sans quitter l'IDE. Pour des flux de travail plus avancés, utilisez le terminal.

---

## Utilisation avancée et exemples de commandes

### Tâches Gradle

Exécutez n'importe quelle tâche Gradle standard via le terminal :

```bash
# Nettoyer les artefacts de build
./gradlew clean

# Assembler un APK de version (non signé)
./gradlew assembleRelease

# Exécuter les vérifications lint
./gradlew lint

# Exécuter les tests unitaires
./gradlew testDebugUnitTest
```

### Signer un APK de version

AndroidIDE fournit un **Gestionnaire de Keystore** :

1. Allez dans **Build → Signature et Keystores**.
2. Créez un nouveau keystore ou importez un existant.
3. Configurez la signature de version comme vous le feriez dans `app/build.gradle.kts` :

```kotlin
android {
    ...
    signingConfigs {
        create("release") {
            keyAlias = "releasekey"
            keyPassword = "..."
            storeFile = file("/path/to/keystore.jks")
            storePassword = "..."
        }
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

Ensuite, compilez : `./gradlew assembleRelease`

L'APK signé sera généré dans `app/build/outputs/apk/release/`.

### Construction d'Android App Bundles (AAB)

Pour produire un AAB destiné à la distribution sur Google Play :

```bash
./gradlew bundleRelease
```

Le fichier AAB est disponible à l'adresse `app/build/outputs/bundle/release/app-release.aab`.

### Variantes de build personnalisées

Définissez des flavors et des types de build dans votre script Gradle ; tous sont accessibles via la convention de dénomination habituelle de Gradle :

```bash
./gradlew assembleFlavorDebug
./gradlew assembleFlavorRelease
```

---

## Structure du projet et compatibilité

AndroidIDE fonctionne avec **les projets Android Studio standard**. Un arbre de projet typique est entièrement pris en charge :

```
project/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/...
│   │   │   ├── res/...
│   │   │   └── AndroidManifest.xml
│   │   ├── test/...
│   │   └── androidTest/...
│   ├── build.gradle.kts (ou .groovy)
│   └── proguard-rules.pro
├── gradle/
│   └── wrapper/
├── build.gradle.kts
├── settings.gradle.kts
└── gradlew
```

Vous pouvez **importer des projets existants** via le bouton **Ouvrir le projet** ou en copiant le dossier du projet dans l'espace de travail par défaut (`AndroidIDE/Projects/`).

> **Remarque** : Les projets utilisant la version 6.0+ du wrapper Gradle sont recommandés pour une meilleure compatibilité. Les projets basés sur NDK/CMake fonctionnent également, mais les temps de build peuvent augmenter considérablement sur du matériel bas de gamme.

---

## Considérations sur les performances

- **Temps de build** – Sur les appareils modernes (par ex., Snapdragon 8 Gen 1), un build debug typique prend 2 à 3 minutes, tandis qu'un build release avec minification peut prendre 5 à 8 minutes. Sur du matériel plus ancien (4 Go de RAM, Helio G80), prévoyez 5 à 10 minutes pour les builds debug.
- **Batterie et chaleur** – La compilation est intensive en CPU ; attendez-vous à une décharge notable de la batterie et à une génération de chaleur. L'utilisation d'un refroidisseur ou une bonne ventilation est conseillée.
- **Mémoire** – Les grands projets (plus de 1000 fichiers sources) peuvent atteindre les limites de mémoire sur les appareils de 4 Go. Fermer les autres applications peut aider.
- **Mises à jour du SDK** – AndroidIDE permet de mettre à jour les composants SDK via le Gestionnaire SDK. Cependant, le téléchargement de gros paquets via les données mobiles n'est pas recommandé.

Malgré ces limitations, le compromis est une portabilité inégalée : un environnement de développement complet dans votre poche.

---

## Historique et développement

AndroidIDE a été créé à l'origine par **terminal_editor** (et maintenu plus tard par l'équipe AndroidIDE). Le projet a attiré l'attention avec **v2.0**, qui a introduit :

- Une réécriture complète du backend de l'IDE.
- Le wrapper Gradle optimisé pour mobile.
- Une interface utilisateur moderne, inspirée de Material You.

Depuis lors, le projet est **activement maintenu sur GitHub** ([github.com/AndroidIDE/AndroidIDE](https://github.com/AndroidIDE/AndroidIDE)), avec des versions fréquentes, des traductions communautaires et des améliorations incrémentales. La dernière version stable actuelle est **v2.7.1-beta** (en date de juin 2026), qui a apporté la disponibilité sur F‑Droid et diverses corrections de stabilité.

AndroidIDE est construit avec une combinaison de **Java/Kotlin** (frontend IDE) et **shell scripts** (orchestration de build). Les contributions sont les bienvenues, et le projet dispose d'une communauté Discord active.

---

## Conclusion

AndroidIDE prouve que le développement d'applications Android n'est plus lié à un ordinateur de bureau. Avec son intégration Gradle complète, son éditeur de code intelligent et ses outils de débogage intégrés, c'est un environnement puissant pour quiconque souhaite créer, tester et publier des applications en utilisant uniquement un appareil mobile. Bien qu'il ne puisse pas égaler la vitesse d'un bureau à 8 cœurs, sa commodité et sa nature open-source en font un outil inestimable pour le développeur moderne axé sur le mobile.

**Commencez dès aujourd'hui**

- Téléchargez depuis GitHub : [AndroidIDE/releases](https://github.com/AndroidIDE/AndroidIDE/releases)
- Source et problèmes : [AndroidIDE/AndroidIDE](https://github.com/AndroidIDE/AndroidIDE)
- F‑Droid (v2.7.1+) : recherchez « AndroidIDE » dans le magasin F‑Droid.

---