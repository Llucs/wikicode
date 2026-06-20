---
title: Lazygit – The Terminal Git UI That Boosts Your Productivity
description: A comprehensive guide to lazygit, a terminal-based Git UI that simplifies complex Git operations like staging, rebasing, and conflict resolution via an intuitive, keyboard-driven interface.
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – The Terminal Git UI That Boosts Your Productivity

**Lazygit** is a cross-platform, keyboard-driven Terminal User Interface (TUI) for Git. Created by Jesse Duffield in 2018 and written in Go, it wraps Git's most complex—and often error-prone—operations into an intuitive, panel-based layout that lives entirely inside your terminal.

> "Stop memorizing Git commands. Start using Git intuitively."

---

## Why Lazygit?

Git's command-line interface is powerful but notoriously unforgiving. Interactive rebasing, staging hunks, resolving conflicts, and managing branches all require precise sequences of commands. Lazygit solves this by:

- **Visualizing Your Repository** – See branches, tags, the commit graph, the working tree, and stash at a glance.
- **Speeding Up Daily Work** – Stage, commit, push, and pull without typing a single `git` command.
- **Reducing Mistakes** – Interactive rebasing, cherry-picking, and conflict resolution become menu-driven and undoable.
- **Lowering the Learning Curve** – New team members can perform advanced Git operations immediately, freeing them from memorizing arcane syntax.
- **Working Cross-Platform** – Runs on Linux, macOS, and Windows with the same interface and keybindings.

---

## Installation

Lazygit is available through most package managers. Pick your platform:

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

## Basic Usage

Navigate into any Git repository and launch:

```bash
cd my-project
lazygit
```

Lazygit opens with a split-panel layout. The left column shows (from top to bottom) the **Status**, **Files**, **Branches**, **Commits**, and **Stash** panels. The right side displays the diff or log for the selected item.

### Panel Navigation

| Key | Action |
|-----|--------|
| `←` / `→` | Move between panels |
| `Tab` | Cycle panels forward |
| `Shift + Tab` | Cycle panels backward |
| `j` / `k` | Move up/down inside a panel |
| `J` / `K` | Scroll the main diff panel |
| `?` | Show/hide full keybindings help |

### Quick Start (Daily Workflow)

1. **Launch** – Run `lazygit` inside a repo.
2. **Stage a file** – Press `Space` on a file in the Files panel.
3. **Stage a specific hunk** – Press `Enter` to view the diff, then `Space` on individual hunks.
4. **Commit** – Press `c`, type a message, and press `Enter`.
5. **Push** – Press `P` (upper case) to push.
6. **Pull** – Press `p` (lower case) to pull.
7. **Quit** – Press `q` to exit.

---

## Key Features (with Command Examples)

### 🎯 Interactive Staging (Better Than `git add -p`)

View a file's diff, then stage/unstage individual lines or hunks visually. No more counting cursor positions.

```bash
# Inside the Files panel:
# Enter  → open the file diff
# Space  → stage the selected hunk
# a      → stage all changes
# Enter on a specific hunk → stage individual lines
```

### 🔁 Interactive Rebase (The Killer Feature)

Reorder, squash, fixup, edit, or drop commits with single keystrokes.

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

After marking, press `Enter` to confirm. Lazygit executes the rebase and shows progress. If conflicts occur, it jumps to the conflict resolution panel.

### ↩️ Undo / Redo (Safety Net)

Lazygit tracks its own internal action history. Made a mistake during a rebase or accidentally dropped a commit? Undo it.

```bash
# z  → undo last action
# Z (Shift+z)  → redo
```

### 🌳 Branch Management

Switch, merge, rebase, rename, and delete branches without leaving the UI.

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

Copy commits from one branch to another without `git log` or commit hash hunting.

```bash
# In the Commits panel:
# c        → start cherry-pick mode
# Space    → toggle selection of a commit
# Shift+c  → complete cherry-pick
```

### 🧩 Stash Management

Name stashes, apply them, pop them, and even create branches from stashes.

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

### ⚔️ Conflict Resolution

When a rebase or merge produces conflicts, Lazygit shows a three‑way diff with inline conflict markers. Resolve them visually.

```bash
# Conflict panel will open automatically:
# Ctrl+o → open file in external merge tool
# Space  → stage resolved file
# Enter  → edit file manually
# /      → search for remaining conflict markers
```

### 🌳 Worktree Support

Lazygit has first-class support for Git worktrees, letting you add, remove, and switch between them.

```bash
# In the Branches panel (or dedicated Worktrees panel):
# w        → open worktree management
# a        → add a new worktree
# d        → remove a worktree
# Space    → switch to a worktree
```

### 🧹 Custom Commands

Extend Lazygit with your own shell commands or scripts that appear in the UI.

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

## Pro Tips

1. **Vim‑adjacent keybindings** – `j/k` to navigate, `J/K` to scroll diffs, `/` to search inside panels.
2. **Filter files** – Type `/` in the Files panel to filter by filename.
3. **Diff against a specific commit** – In the Commits panel, press `d` on a commit to see what changed in that commit.
4. **Toggle diff visibility** – Press `Ctrl+d` to cycle through diff display modes.
5. **Use with your existing Git config** – Lazygit respects your aliases, difftool, and merge tool settings.

---

## Configuration

Lazygit is highly configurable. A full config file lives at:

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

Generate a template with:

```bash
lazygit --print-config
```

Common settings include keybindings overrides, theme colors, custom commands, and UI layout.

---

## When to Reach for Lazygit

| Scenario | Why Lazygit Shines |
|----------|-------------------|
| Interactive rebasing | Visual commit selection and reordering; undo available |
| Staging partial changes | Line‑by‑line hunk selection with instant diff |
| Onboarding new devs | No need to memorize complex Git commands |
| Code review prep | Create clean, logical commit series in minutes |
| Conflict resolution | Three‑way diff viewer with inline action |
| Repository overview | See branches, tags, remotes, stash, and commit graph at once |

---

## Resources

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **Documentation:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **Config Reference:** [lazygit Configuration](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **Author's "lazy" ecosystem:** Lazygit, Lazydocker, Lazynpm – all following the same TUI philosophy.

---

Lazygit doesn't replace Git; it makes it accessible, visual, and fast. Whether you're a seasoned Git power user or a developer who just wants to get back to writing code, Lazygit will save you hours every week. Give it one day—you'll never want to go back to plain `git rebase -i` again.