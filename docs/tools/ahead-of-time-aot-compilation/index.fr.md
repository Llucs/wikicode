---
title: Compilation anticipée (AOT)
description: Une technique d'optimisation de build où le code est compilé avant l'exécution pour améliorer les performances, le démarrage instantané et des déploiements plus légers.
created: 2026-06-21
tags:
  - compilation
  - aot
  - native-image
  - performance
  - graalvm
  - dotnet
  - go
  - rust
status: draft
---

# Compilation anticipée (AOT)

## Qu'est-ce que la compilation anticipée ?

La compilation anticipée (AOT) est le processus de traduction d'un langage de programmation de haut niveau ou d'une représentation intermédiaire (comme le .NET IL, le bytecode Java ou le LLVM IR) en code machine natif **avant** l'exécution, généralement au moment de la construction. Cela contraste avec la compilation Just-in-Time (JIT) qui effectue la compilation au moment de l'exécution.

Des langages comme C, C++, Go et Rust sont intrinsèquement compilés en AOT. Les langages gérés modernes supportent également l'AOT via des chaînes d'outils spécialisées, telles que GraalVM Native Image pour Java, NativeAOT pour .NET et Angular AOT pour TypeScript.

## Pourquoi utiliser la compilation AOT ?

L'AOT offre plusieurs avantages clés par rapport à l'exécution JIT ou interprétée :

- **Démarrage instantané** – Aucune phase de préchauffage ; le code natif s'exécute immédiatement.
- **Performance déterministe** – Pas de pauses JIT pendant l'exécution, réduisant la tail latency.
- **Empreinte mémoire réduite** – Aucun compilateur JIT ou données de compilation à l'exécution nécessaires.
- **Déploiements plus légers** – Les exécutables liés statiquement en un seul fichier conduisent à des images conteneur minimales.
- **Optimisation du démarrage à froid** – Essentiel pour les applications serverless, edge et conteneurisées.

## Installation

La chaîne d'outils AOT varie selon la plateforme. Vous trouverez ci-dessous des configurations courantes :

### GraalVM Native Image (Java)

1. Téléchargez GraalVM depuis [graalvm.org](https://graalvm.org).
2. Définissez `JAVA_HOME` et ajoutez `bin` au `PATH`.
3. Installez l'outil `native-image` :
   ```bash
   gu install native-image
   ```

### .NET NativeAOT

Nécessite .NET 7 ou version ultérieure (prise en charge complète dans .NET 8+). La charge de travail est incluse dans le SDK.

### Go (AOT par défaut)

Aucune installation supplémentaire – le compilateur standard `go` effectue la compilation AOT.

### Rust (AOT par défaut)

Installez via `rustup` (par exemple, `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`).

## Utilisation

### Java avec GraalVM Native Image

```bash
native-image -jar myapp.jar myapp-native
```

Exemple de sortie :
```
================================================================================
GraalVM Native Image: Generating 'myapp-native' (executable)...
================================================================================
```

### .NET NativeAOT

```bash
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
```

La sortie est un exécutable natif autonome dans le répertoire `bin/Release/net8.0/linux-x64/publish/`.

### Go (AOT implicite)

```bash
go build -o myapp main.go
```

Le binaire produit est autonome et s'exécute immédiatement sans environnement d'exécution.

### Rust

```bash
cargo build --release
```

Le binaire résultant dans `target/release/` est compilé en AOT et bénéficie souvent de l'optimisation guidée par profil (PGO) pour des performances encore meilleures.

## Caractéristiques principales

### 1. Zéro préchauffage

Comme tout le code est déjà compilé, les applications démarrent et atteignent des performances de pointe instantanément.

*Exemple (Java) :*
```bash
time java -jar myapp.jar      # JIT – may take seconds
time ./myapp-native           # AOT – starts in milliseconds
```

### 2. Latence déterministe

Pas de pauses liées au GC et au JIT. Critique pour les systèmes en temps réel, les plateformes de trading et le trading haute fréquence.

### 3. Empreinte réduite

- **GraalVM Native Image** peut réduire la taille de l'image de >200 Mo (JVM+app) à <20 Mo.
- **.NET NativeAOT** produit des binaires qui n'incluent que les composants d'exécution nécessaires.

### 4. Élimination du code mort

Les analyseurs AOT suppriment le code inaccessible, ce qui donne des exécutables plus petits et une sécurité améliorée.

### 5. Optimisation guidée par profil (PGO)

Combinée avec l'AOT, les données de profil PGO collectées lors d'exécutions de test peuvent être utilisées au moment de la construction pour optimiser davantage le binaire.

*Exemple (Rust) :*
```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# Run training workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data" cargo build --release
```

## Limitations

- **Réflexion / chargement dynamique** – Doit être configuré explicitement (par exemple, `reflect-config.json` pour Native Image).
- **Temps de construction** – La compilation AOT est plus lente que la JIT.
- **Performances de pointe** – La JIT de longue durée avec profilage peut encore surpasser l'AOT sur des charges de travail intensives en CPU.
- **Prise en charge** – Toutes les bibliothèques et frameworks ne sont pas compatibles avec l'AOT.

## Conclusion

La compilation AOT est une technique fondamentale pour les applications cloud-native, serverless et edge modernes. En sacrifiant une certaine flexibilité à l'exécution, elle offre une vitesse de démarrage inégalée, des performances prévisibles et une utilisation minimale des ressources. Des outils comme GraalVM Native Image, .NET NativeAOT, Go et Rust rendent l'AOT accessible et pratique pour une utilisation en production.