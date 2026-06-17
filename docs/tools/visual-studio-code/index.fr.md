---
title: Visual Studio Code
description: Un éditeur de code source léger mais puissant développé par Microsoft qui sert d'outil de développement intégré.
created: 2026-06-14
tags:
  - editor
  - development
  - microsoft
  - open-source
status: draft
ecosystem: editors
---

# Visual Studio Code

## Qu'est-ce que VS Code ?

Visual Studio Code (souvent appelé VS Code) est un éditeur de code source gratuit et open‑source développé par Microsoft. Construit sur le framework Electron, il fonctionne sur Windows, macOS et Linux. VS Code combine la rapidité et la simplicité d'un éditeur léger avec les capacités avancées d'un environnement de développement intégré (IDE) grâce à une riche architecture d'extensions.

## Pourquoi VS Code ?

- **Performance** : Démarre rapidement et reste réactif même avec de grands projets.
- **Extensibilité** : Des milliers d'extensions ajoutent des langages, des thèmes, des débogueurs et des outils de workflow.
- **Multi‑plateforme** : Même expérience sur tous les systèmes d'exploitation majeurs.
- **Outillage intégré** : Contrôle Git, terminal, débogage – le tout depuis l'éditeur.
- **Édition intelligente** : IntelliSense fournit des complétions contextuelles, des informations sur les paramètres et de la documentation.
- **Prise en charge intégrée des workflows modernes** : Docker, développement à distance, notebooks Jupyter, et plus encore.

## Installation

### Télécharger l'installateur
Le moyen le plus simple est de télécharger l'installateur depuis le [site officiel](https://code.visualstudio.com).

| Plateforme | Type d'installateur |
|------------|---------------------|
| Windows    | `.exe` (utilisateur ou système) |
| macOS      | `.dmg` (glisser vers Applications) |
| Linux      | `.deb` (Debian/Ubuntu) ou `.rpm` (Fedora/RHEL) |

### Gestionnaires de paquets

**macOS (Homebrew)**
```bash
brew install --cask visual-studio-code
```

**Linux (Snap)**
```bash
snap install code --classic
```

**Windows (winget)**
```bash
winget install Microsoft.VisualStudioCode
```

### Mode portable
Créez un dossier `data` dans le même répertoire que l'exécutable VS Code. L'éditeur stockera toute la configuration, les extensions et les données utilisateur dans ce dossier, le rendant ainsi entièrement portable.

### Version Insiders
Pour un accès anticipé aux fonctionnalités et aux builds quotidiens, installez [VS Code Insiders](https://code.visualstudio.com/insiders). Il peut être installé côte à côte avec la version stable.

## Utilisation de base

### Ouvrir un projet
Lancez VS Code et utilisez **Fichier → Ouvrir un dossier** (ou `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`) pour ouvrir votre répertoire de projet.

### Palette de commandes
La palette de commandes donne accès à toutes les actions dans VS Code.

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

Commandes courantes : `>Format Document`, `>Preferences: Open Settings`, `>Extensions: Install Extensions`.

### Modifier des fichiers
- La coloration syntaxique est automatique selon l'extension du fichier.
- **Multi‑curseur** : `Alt+Clic` (Windows/Linux) ou `Option+Clic` (macOS) pour ajouter des curseurs.
- **Correspondance des parenthèses** : Déplacez le curseur à l'intérieur des parenthèses, la paire correspondante est mise en évidence.
- **IntelliSense** : Déclenchez‑le manuellement avec `Ctrl+Espace`.

### Contrôle de version
Ouvrez la vue Contrôle de source (`Ctrl+Shift+G` sur Windows/Linux, `Cmd+Shift+G` sur macOS) pour voir les modifications, indexer les fichiers, valider et effectuer des push/pull. Utilisez le terminal intégré pour des opérations plus complexes.

### Terminal intégré
Lancez le terminal avec `` Ctrl+` `` (accent grave). Le terminal utilise par défaut le shell de votre système (PowerShell, bash, zsh, etc.).

### Extensions
Ouvrez la vue Extensions avec `Ctrl+Shift+X`. Recherchez une extension (par exemple « Python », « Prettier », « Docker ») et installez‑la en un clic.

### Débogage
Placez des points d'arrêt en cliquant dans la gouttière (zone des numéros de ligne) ou en appuyant sur `F9`. Appuyez sur `F5` pour démarrer le débogage avec la configuration active. Créez un fichier `launch.json` pour configurer les paramètres de débogage de votre projet.

## Fonctionnalités clés avec exemples de commandes

### IntelliSense
VS Code fournit des complétions intelligentes basées sur les services de langage, les types de variables et les définitions de fonctions.

```javascript
// Exemple : saisir "console." puis utiliser Ctrl+Espace affiche des méthodes comme log, warn, error
console.log("Hello, VS Code !");
```

**Déclencher IntelliSense manuellement** : `Ctrl+Espace` (Windows/Linux) ou `Cmd+Espace` (macOS).

**Indices de paramètres** : Lors de l'appel d'une fonction, VS Code affiche les paramètres attendus.

### Débogage intégré
Prise en charge complète du débogage avec des configurations de lancement.

**Exemple de launch.json pour Node.js :**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Lancer le programme",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/app.js"
        }
    ]
}
```

**Commandes de débogage essentielles :**
| Action | Touches |
|--------|---------|
| Démarrer/Continuer | `F5` |
| Pas à pas principal | `F10` |
| Pas à pas détaillé | `F11` |
| Pas à pas sortant | `Shift+F11` |
| Activer/désactiver un point d'arrêt | `F9` |

### Git intégré
Contrôle de source visuel avec indexation, validation, branchement, etc.

**Équivalents dans la palette de commandes :**
- `>Git: Commit` – valider les modifications indexées.
- `>Git: Create Branch` – créer une nouvelle branche.
- `>Git: Clone` – cloner un dépôt distant.
- `>Git: Pull` / `Git: Push` – synchroniser les modifications.

### Marketplace d'extensions
Installez des extensions pour ajouter des langages, des linters, des thèmes, des extraits de code et des débogueurs.

**Exemple : Installer l'extension Python**
1. Ouvrez la vue Extensions (`Ctrl+Shift+X`).
2. Recherchez « Python » (par Microsoft).
3. Cliquez sur **Installer**.

**Extensions populaires :**
- Python
- Prettier – Formateur de code
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### Terminal intégré
Exécutez des commandes shell sans quitter VS Code.

```bash
# Exemple : dans le terminal intégré
npm install && npm start
```

Ouvrez/fermez le terminal avec `` Ctrl+` ``. Plusieurs terminaux peuvent être créés (par exemple, un pour la construction, un pour git).

### Développement à distance
Connectez‑vous à des environnements distants tels que :
- **WSL** (Windows Subsystem for Linux)
- Machines distantes **SSH**
- **Conteneurs de développement** (Docker)
- **GitHub Codespaces**

**Exemples dans la palette de commandes :**
- `>Remote‑SSH: Connect to Host…`
- `>Dev Containers: Reopen in Container`

Pas besoin de quitter l'éditeur – votre environnement de développement complet est accessible localement.

## Conseils supplémentaires

### Synchronisation des paramètres
Connectez‑vous avec un compte Microsoft ou GitHub et vos paramètres, raccourcis clavier et extensions sont synchronisés entre vos machines.

**Palette de commandes** : `>Turn on Settings Sync…`

### Extraits de code
Créez des extraits de code personnalisés pour les motifs répétitifs.

**Fichier → Préférences → Configurer les extraits de code utilisateur** → choisissez un langage.

```json
// Exemple d'extrait JavaScript (dans javascript.json)
{
    "Fonction fléchée": {
        "prefix": "arr",
        "body": ["const ${1:name} = (${2:params}) => {", "\t${3:body}", "};"],
        "description": "Créer une fonction fléchée"
    }
}
```

### Édition multi‑curseur
- `Alt+Clic` – ajouter un curseur.
- `Ctrl+Alt+Haut/Bas` – insérer un curseur au‑dessus/en dessous.
- `Ctrl+D` – sélectionner l'occurrence suivante de la sélection actuelle.

### Mode Zen
Concentrez‑vous sur le code sans distractions : `Ctrl+K Z` (Windows/Linux) ou `Cmd+K Z` (macOS). Quittez avec `Esc Esc`.

## Conclusion

Visual Studio Code est un éditeur polyvalent qui équilibre rapidité, puissance et personnalisation. En maîtrisant ses fonctionnalités principales – IntelliSense, débogage, intégration Git, terminal et écosystème d'extensions – vous pouvez rationaliser votre workflow de développement, quel que soit le langage ou la plateforme.

Pour une exploration plus approfondie, consultez la [documentation officielle de VS Code](https://code.visualstudio.com/docs).