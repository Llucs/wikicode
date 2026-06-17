---
title: fzf - Recherche floue en ligne de commande
description: Un outil de recherche floue en ligne de commande qui améliore la recherche de fichiers et de texte dans le terminal.
created: 2026-06-15
tags:
  - command-line
  - fuzzy-finder
  - fzf
  - productivity
  - terminal
status: draft
ecosystem: cli
---

# fzf – Chercheur flou en ligne de commande à usage général

fzf est un **chercheur flou** interactif qui apporte la puissance de la recherche incrémentale à toute liste présentée en ligne de commande. Écrit à l'origine en Ruby puis réécrit en Go par [Junegunn Choi](https://github.com/junegunn), il est devenu un outil essentiel pour les développeurs, les administrateurs système et les utilisateurs avancés qui souhaitent naviguer dans les fichiers, les commandes, les processus, etc., à une vitesse fulgurante.

Au lieu de taper des noms exacts ou de se fier uniquement à la complétion par tabulation, fzf vous permet de taper n'importe quelle sous-chaîne (ou même une séquence floue) et filtre instantanément l'entrée. Il fonctionne avec n'importe quelles données transmises via stdin et renvoie l'élément sélectionné sur stdout, ce qui en fait un choix parfait pour les pipelines Unix.

---

## Pourquoi utiliser fzf ?

- **Rapidité** : gère des centaines de milliers d'entrées en temps quasi réel.
- **Correspondance floue** : trouvez des fichiers et des commandes sans mémoriser les noms exacts.
- **Interactivité** : filtrage en direct avec retour visuel immédiat.
- **Composabilité** : fonctionne avec toute commande qui produit ou consomme du texte.
- **Personnalisation** : thèmes, raccourcis clavier, fenêtres d'aperçu, etc.

---

## Installation

### macOS
```bash
brew install fzf
# Install useful key bindings and fuzzy auto-completion
$(brew --prefix)/opt/fzf/install
```

### Linux (Debian/Ubuntu)
```bash
sudo apt install fzf           # Often outdated – prefer building from source
# Or from the official repository:
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Arch Linux
```bash
sudo pacman -S fzf
```

### Windows (WSL / Git Bash / Scoop)
```bash
scoop install fzf
# Or with Chocolatey
choco install fzf
```

### Go (any platform)
```bash
go install github.com/junegunn/fzf@latest
```

---

## Utilisation de base

### Transmettre une liste à fzf
```bash
# Search through all files in the current directory
find . -type f | fzf
```

### Sélectionner un fichier et l'ouvrir dans un éditeur
```bash
vim "$(find . -type f | fzf)"
```

### Aperçu du contenu des fichiers
```bash
fzf --preview 'cat {}'       # {} is the path of the current item
```

### Disposition inversée (recherche en bas)
```bash
fzf --reverse
```

### Sélection multiple (avec Tab)
```bash
fzf --multi
```

### Invite personnalisée
```bash
fzf --prompt="Pick a file> "
```

---

## Fonctionnalités principales

### Modes de correspondance floue
fzf prend en charge plusieurs modes de correspondance pour affiner votre recherche :

- **Flou (par défaut)** : `abc` correspond à `alphabet.txt` – toute séquence de sous-chaînes fonctionne.
- **Correspondance exacte** : préfixez avec `'` → `'abc` ne correspond qu'aux lignes contenant exactement « abc ».
- **Correspondance par préfixe** : suffixez avec `^` → `^abc` correspond aux lignes commençant par « abc ».
- **Correspondance par suffixe** : préfixez avec `$` → `abc$` correspond aux lignes se terminant par « abc ».
- **Expression régulière** : préfixe `!` pour inverser, ou utilisez l'intégration `rg`.

### Fenêtre d'aperçu
La fenêtre d'aperçu affiche des informations contextuelles pour l'élément sélectionné. Elle peut utiliser des commandes externes comme `cat`, `bat`, `head`, ou même des scripts personnalisés :

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### Intégration au shell
Le script d'installation officiel met en place trois raccourcis clavier pratiques (Bash, Zsh, Fish) :

| Raccourci | Action |
|-----------|--------|
| `Ctrl+R` | Rechercher dans l'historique des commandes |
| `Ctrl+T` | Rechercher des fichiers/répertoires et coller leurs chemins |
| `Alt+C`  | Sauter dans un sous-répertoire (cd flou) |

### Plugin Vim / Neovim
fzf fournit un plugin Vim natif. L'extension la plus populaire est [fzf.vim](https://github.com/junegunn/fzf.vim), qui ajoute des commandes telles que :

| Commande | Objectif |
|----------|----------|
| `:Files [path]` | Rechercher des fichiers |
| `:Rg [pattern]` | Rechercher le contenu des fichiers (nécessite ripgrep) |
| `:Buffers` | Basculer entre les tampons ouverts |
| `:GFiles?` | Rechercher les fichiers non suivis dans un dépôt Git |
| `:Commands` | Lister les commandes Vim |
| `:Maps` | Afficher les mappages de touches |

### Extensibilité
Parce que fzf fonctionne sur stdin/stdout, il s'intègre parfaitement dans n'importe quel flux de travail. Vous pouvez l'envelopper dans des fonctions shell ou des scripts pour créer vos propres menus interactifs.

---

## Cas d'utilisation avancés

### Tueur de processus
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### Changer de branche Git
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### Se connecter en SSH à des hôtes depuis le fichier de configuration
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### Rechercher dans le contenu des fichiers avec aperçu
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### Changer de répertoire interactivement (avec fd)
```bash
cd "$(fd --type d | fzf)"
```
Ou utilisez le raccourci intégré `Alt+C`.

### Recherche de conteneurs Docker
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## Trucs et astuces

- **Utilisez l'option `--header`** pour afficher des instructions :
  ```bash
  fzf --header "Press Ctrl-R for history, Ctrl-T for files"
  ```

- **Stockez les éléments sélectionnés dans une variable** pour des opérations par lots.

- **Ajoutez un aperçu en couleur** en utilisant `bat` ou `highlight` avec le support ANSI.

- **Combinez avec `tmux`** pour ouvrir le panneau d'aperçu dans un volet séparé.

- **Personnalisez le jeu de couleurs** via la variable d'environnement `FZF_DEFAULT_OPTS` :
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## Conclusion

fzf est un outil de référence pour la recherche interactive dans le terminal. Sa correspondance floue, sa rapidité et sa composabilité le rendent indispensable pour quiconque vit en ligne de commande. Que vous parcouriez des fichiers, traquiez des processus ou construisiez des workflows personnalisés, fzf transforme les tâches de recherche fastidieuses en une expérience fluide, presque magique.

Pour la documentation complète, visitez le [dépôt GitHub](https://github.com/junegunn/fzf).