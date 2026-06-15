---
title: fzf - Command-Line Fuzzy Finder
description: A command-line fuzzy finder tool that enhances file and text searching in the terminal.
created: 2026-06-15
tags:
  - command-line
  - fuzzy-finder
  - fzf
  - productivity
  - terminal
status: draft
---

# fzf – General-Purpose Command-Line Fuzzy Finder

fzf is an interactive **fuzzy finder** that brings the power of incremental search to any list presented on the command line. Originally written in Ruby and later rewritten in Go by [Junegunn Choi](https://github.com/junegunn), it has become an essential tool for developers, sysadmins, and power users who want to navigate files, commands, processes, and more with lightning speed.

Instead of typing exact names or relying on tab-completion alone, fzf lets you type any substring (or even a fuzzy sequence) and instantly filters the input. It works with any data streamed through stdin and returns the selected item on stdout, making it a perfect fit for Unix pipelines.

---

## Why Use fzf?

- **Speed**: Handles hundreds of thousands of entries in near real‑time.
- **Fuzzy Matching**: Find files and commands without remembering exact names.
- **Interactivity**: Live filtering with immediate visual feedback.
- **Composability**: Works with any command that produces or consumes text.
- **Customizability**: Themes, key bindings, preview windows, and more.

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

## Basic Usage

### Pipe a list to fzf
```bash
# Search through all files in the current directory
find . -type f | fzf
```

### Select a file and open it in an editor
```bash
vim "$(find . -type f | fzf)"
```

### Preview file contents
```bash
fzf --preview 'cat {}'       # {} is the path of the current item
```

### Reverse layout (search at bottom)
```bash
fzf --reverse
```

### Multi-select (with Tab)
```bash
fzf --multi
```

### Custom prompt
```bash
fzf --prompt="Pick a file> "
```

---

## Key Features

### Fuzzy Matching Modes
fzf supports several matching modes to fine‑tune your search:

- **Fuzzy (default)**: `abc` matches `alphabet.txt` – any substring sequence works.
- **Exact match**: prefix with `'` → `'abc` matches only lines containing exactly “abc”.
- **Prefix match**: suffix with `^` → `^abc` matches lines starting with “abc”.
- **Suffix match**: prefix with `$` → `abc$` matches lines ending with “abc”.
- **Regular expression**: `!` prefix to invert, or use `rg` integration.

### Preview Window
The preview window shows contextual information for the highlighted item. It can use external commands like `cat`, `bat`, `head`, or even custom scripts:

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### Shell Integration
The official `install` script sets up three handy key bindings (Bash, Zsh, Fish):

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Search command history |
| `Ctrl+T` | Search files/directories and paste their paths |
| `Alt+C`  | Jump into a subdirectory (fuzzy cd) |

### Vim / Neovim Plugin
fzf provides a native Vim plugin. The most popular extension is [fzf.vim](https://github.com/junegunn/fzf.vim), which adds commands such as:

| Command | Purpose |
|---------|---------|
| `:Files [path]` | Search files |
| `:Rg [pattern]` | Search file contents (requires ripgrep) |
| `:Buffers` | Switch between open buffers |
| `:GFiles?` | Search untracked files in a Git repository |
| `:Commands` | List Vim commands |
| `:Maps` | Show key mappings |

### Extensibility
Because fzf operates on stdin/stdout, it integrates seamlessly into any workflow. You can wrap it in shell functions or scripts to create your own interactive menus.

---

## Advanced Use Cases

### Process Killer
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### Checkout a Git Branch
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### SSH into Hosts from Config
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### Search File Contents with Preview
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### Interactively Change Directory (with fd)
```bash
cd "$(fd --type d | fzf)"
```
Or use the built‑in `Alt+C` binding.

### Docker Container Search
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## Tips & Tricks

- **Use the `--header` option** to show instructions:
  ```bash
  fzf --header "Press Ctrl-R for history, Ctrl-T for files"
  ```
- **Store selected items in a variable** for batch operations.
- **Add a colored preview** by using `bat` or `highlight` with ANSI support.
- **Combine with `tmux`** to open the preview pane in a separate split.
- **Customize the color scheme** via `FZF_DEFAULT_OPTS` environment variable:
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## Conclusion

fzf is a gold standard tool for interactive terminal searching. Its fuzzy matching, speed, and composability make it indispensable for anyone who lives in the command line. Whether you’re browsing files, hunting down processes, or building custom workflows, fzf turns tedious lookup tasks into a fluid, almost magical experience.

For full documentation, visit the [GitHub repository](https://github.com/junegunn/fzf).