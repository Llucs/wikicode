---
title: Lazygit – L'interface Git en terminal qui booste votre productivité
description: Un guide complet de lazygit, une interface Git en terminal qui simplifie les opérations Git complexes comme le staging, le rebase et la résolution de conflits via une interface intuitive et pilotée au clavier.
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – L'interface Git en terminal qui booste votre productivité

**Lazygit** est une interface utilisateur en terminal (TUI) multiplateforme et pilotée au clavier pour Git. Créé par Jesse Duffield en 2018 et écrit en Go, il encapsule les opérations les plus complexes—et souvent sujettes à erreur—de Git dans une disposition intuitive basée sur des panneaux qui vit entièrement dans votre terminal.

> "Arrêtez de mémoriser les commandes Git. Commencez à utiliser Git de manière intuitive."

---

## Pourquoi Lazygit ?

L'interface en ligne de commande de Git est puissante mais notoirement impitoyable. Le rebase interactif, le staging de hunks, la résolution de conflits et la gestion des branches nécessitent tous des séquences précises de commandes. Lazygit résout ce problème en :

- **Visualisant votre dépôt** – Voyez branches, tags, le graphe des commits, l'arbre de travail et le stash en un coup d'œil.
- **Accélérant le travail quotidien** – Stage, commit, push et pull sans taper une seule commande `git`.
- **Réduisant les erreurs** – Le rebase interactif, le cherry-pick et la résolution de conflits deviennent pilotés par menus et annulables.
- **Abaissant la courbe d'apprentissage** – Les nouveaux membres de l'équipe peuvent effectuer des opérations Git avancées immédiatement, les libérant de la mémorisation d'une syntaxe obscure.
- **Fonctionnant multiplateforme** – Fonctionne sur Linux, macOS et Windows avec la même interface et les mêmes raccourcis clavier.

---

## Installation

Lazygit est disponible via la plupart des gestionnaires de paquets. Choisissez votre plateforme :

```bash
# macOS (Homebrew)
brew install lazygit

# Ubuntu / Debian
sudo add-apt-repository ppa:lazygit-team/release
sudo apt update
sudo apt install lazygit

# Arch Linux
pacman -S lazygit

# Windows
winget install lazygit
# or
scoop install lazygit

# Go (requires Go 1.16+)
go install github.com/jesseduffield/lazygit@latest

# Binary downloads (all platforms)
# https://github.com/jesseduffield/lazygit/releases
```

---

## Utilisation de base

Naviguez dans n'importe quel dépôt Git et lancez :

```bash
cd my-project
lazygit
```

Lazygit s'ouvre avec une disposition en panneaux divisés. La colonne de gauche affiche (de haut en bas) les panneaux **Status**, **Files**, **Branches**, **Commits** et **Stash**. Le côté droit affiche le diff ou le log de l'élément sélectionné.

### Navigation entre les panneaux

| Touche | Action |
|--------|--------|
| `←` / `→` | Se déplacer entre les panneaux |
| `Tab` | Parcourir les panneaux vers l'avant |
| `Shift + Tab` | Parcourir les panneaux vers l'arrière |
| `j` / `k` | Monter/descendre dans un panneau |
| `J` / `K` | Faire défiler le panneau diff principal |
| `?` | Afficher/masquer l'aide complète des raccourcis clavier |

### Démarrage rapide (flux de travail quotidien)

1. **Lancer** – Exécutez `lazygit` dans un dépôt.
2. **Stager un fichier** – Appuyez sur `Space` sur un fichier dans le panneau Files.
3. **Stager un hunk spécifique** – Appuyez sur `Enter` pour voir le diff, puis `Space` sur les hunks individuels.
4. **Commiter** – Appuyez sur `c`, tapez un message et appuyez sur `Enter`.
5. **Pousser (push)** – Appuyez sur `P` (majuscule) pour pousser.
6. **Tirer (pull)** – Appuyez sur `p` (minuscule) pour tirer.
7. **Quitter** – Appuyez sur `q` pour quitter.

---

## Fonctionnalités clés (avec exemples de commandes)

### 🎯 Interactive Staging (Mieux que `git add -p`)

Visualisez le diff d'un fichier, puis stagez/déstagez des lignes ou des hunks individuellement visuellement. Fini de compter les positions du curseur.

```bash
# Inside the Files panel:
# Enter  → open the file diff
# Space  → stage the selected hunk
# a      → stage all changes
# Enter on a specific hunk → stage individual lines
```

### 🔁 Interactive Rebase (La fonctionnalité incontournable)

Réorganisez, squashez, fixupez, éditez ou supprimez des commits en une seule frappe.

```bash
# Switch to the Commits panel (press 4):
# i       → start interactive rebase
# s       → squash commit into previous
# f       → fixup (squash, discard message)
# d       → drop commit entirely
# e       → edit commit (pause rebase)
# r       → reword commit message
# Ctrl+j  → move commit down in order
# Ctrl+k  → move commit up in order
```

Après avoir marqué, appuyez sur `Enter` pour confirmer. Lazygit exécute le rebase et affiche la progression. En cas de conflits, il bascule vers le panneau de résolution de conflits.

### ↩️ Undo / Redo (Filet de sécurité)

Lazygit suit son propre historique d'actions internes. Vous avez fait une erreur lors d'un rebase ou supprimé accidentellement un commit ? Annulez-la.

```bash
# z  → undo last action
# Z (Shift+z)  → redo
```

### 🌳 Branch Management

Passez d'une branche à l'autre, fusionnez, rebasez, renommez et supprimez des branches sans quitter l'interface.

```bash
# Press 3 to enter the Branches panel:
# Space    → checkout selected branch
# n        → create a new branch (optionally from current HEAD)
# m        → merge selected branch into current
# r        → rebase current branch onto selected
# R        → rename branch
# d        → delete branch (with confirmation)
# Ctrl+r   → update remote branch references
```

### 🍒 Cherry-Pick Commits

Copiez des commits d'une branche à une autre sans `git log` ou chasse aux hash de commit.

```bash
# In the Commits panel:
# c        → start cherry-pick mode
# Space    → toggle selection of a commit
# Shift+c  → complete cherry-pick
```

### 🧩 Stash Management

Nommez les stashes, appliquez-les, popez-les et même créez des branches à partir de stashes.

```bash
# Press 5 to enter the Stash panel:
# g        → toggle stash view
# s        → stash staged changes
# Shift+s  → stash all changes (including untracked files)
# Space    → apply selected stash
# d        → drop stash
# n        → name a new stash
# b        → create branch from stash
```

### ⚔️ Résolution de conflits

Lorsqu'un rebase ou une fusion produit des conflits, Lazygit affiche un diff à trois voies avec des marqueurs de conflit en ligne. Résolvez-les visuellement.

```bash
# Conflict panel will open automatically:
# Ctrl+o → open file in external merge tool
# Space  → stage resolved file
# Enter  → edit file manually
# /      → search for remaining conflict markers
```

### 🌳 Worktree Support

Lazygit offre un support de première classe pour les worktrees Git, vous permettant d'en ajouter, supprimer et basculer entre eux.

```bash
# In the Branches panel (or dedicated Worktrees panel):
# w        → open worktree management
# a        → add a new worktree
# d        → remove a worktree
# Space    → switch to a worktree
```

### 🧹 Custom Commands

Étendez Lazygit avec vos propres commandes shell ou scripts qui apparaissent dans l'interface.

```bash
# In ~/.config/lazygit/config.yml:
customCommands:
  - key: "C"
    command: "git cz"
    description: "Commit with Commitizen"
    context: "files"
    loadingText: "Opening commitizen..."
```

---

## Astuces de pro

1. **Raccourcis de type Vim** – `j/k` pour naviguer, `J/K` pour faire défiler les diffs, `/` pour chercher dans les panneaux.
2. **Filtrer les fichiers** – Tapez `/` dans le panneau Files pour filtrer par nom de fichier.
3. **Diff par rapport à un commit spécifique** – Dans le panneau Commits, appuyez sur `d` sur un commit pour voir ce qui a changé dans ce commit.
4. **Basculer la visibilité du diff** – Appuyez sur `Ctrl+d` pour parcourir les modes d'affichage du diff.
5. **Utilisez avec votre configuration Git existante** – Lazygit respecte vos alias, difftool et paramètres d'outil de fusion.

---

## Configuration

Lazygit est hautement configurable. Un fichier de configuration complet se trouve à :

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

Générez un modèle avec :

```bash
lazygit --print-config
```

Les paramètres courants incluent les surcharges de raccourcis clavier, les couleurs de thème, les commandes personnalisées et la disposition de l'interface.

---

## Quand utiliser Lazygit

| Scénario | Pourquoi Lazygit excelle |
|----------|--------------------------|
| Rebase interactif | Sélection visuelle et réorganisation des commits ; annulation disponible |
| Staging de modifications partielles | Sélection de hunks ligne par ligne avec diff instantané |
| Intégration des nouveaux développeurs | Pas besoin de mémoriser des commandes Git complexes |
| Préparation de revue de code | Créer une série de commits propre et logique en quelques minutes |
| Résolution de conflits | Visionneuse de diff à trois voies avec action en ligne |
| Vue d'ensemble du dépôt | Voir branches, tags, dépôts distants, stash et graphe de commits en un coup d'œil |

---

## Ressources

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **Documentation:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **Référence de configuration:** [lazygit Configuration](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **Écosystème "lazy" de l'auteur :** Lazygit, Lazydocker, Lazynpm – tous suivant la même philosophie TUI.

---

Lazygit ne remplace pas Git ; il le rend accessible, visuel et rapide. Que vous soyez un utilisateur chevronné de Git ou un développeur qui veut juste se remettre à écrire du code, Lazygit vous fera gagner des heures chaque semaine. Accordez-lui une journée — vous ne voudrez plus jamais revenir à un simple `git rebase -i` again.