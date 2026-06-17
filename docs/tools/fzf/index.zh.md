---
title: fzf - 命令行模糊查找器
description: 一个命令行模糊查找工具，增强终端中的文件和文本搜索能力。
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

# fzf – 通用命令行模糊查找器

fzf 是一个交互式**模糊查找器**，将增量搜索的强大功能应用于命令行中呈现的任何列表。它最初由 [Junegunn Choi](https://github.com/junegunn) 用 Ruby 编写，后来用 Go 重写，如今已成为开发者、系统管理员和高级用户不可或缺的工具，他们希望以闪电般的速度浏览文件、命令、进程等。

与输入精确名称或仅依赖 tab 补全不同，fzf 允许您输入任意子字符串（甚至模糊序列）并立即过滤输入。它适用于任何通过 stdin 传输的数据，并在 stdout 上返回选中的项，使其非常适合 Unix 管道。

---

## 为什么使用 fzf？

- **速度**：近乎实时地处理数十万个条目。
- **模糊匹配**：无需记忆确切名称即可查找文件和命令。
- **交互性**：实时过滤并即时提供视觉反馈。
- **可组合性**：适用于任何产生或消费文本的命令。
- **可定制性**：主题、快捷键、预览窗口等。

---

## 安装

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

## 基本用法

### 通过管道将列表传递给 fzf
```bash
# Search through all files in the current directory
find . -type f | fzf
```

### 选择文件并在编辑器中打开
```bash
vim "$(find . -type f | fzf)"
```

### 预览文件内容
```bash
fzf --preview 'cat {}'       # {} is the path of the current item
```

### 反向布局（搜索在底部）
```bash
fzf --reverse
```

### 多选（使用 Tab 键）
```bash
fzf --multi
```

### 自定义提示符
```bash
fzf --prompt="Pick a file> "
```

---

## 主要特性

### 模糊匹配模式
fzf 支持多种匹配模式以精细调整搜索：

- **模糊匹配（默认）**：`abc` 匹配 `alphabet.txt` – 任何子串序列均可。
- **精确匹配**：前缀 `'` → `'abc` 仅匹配完全包含 “abc” 的行。
- **前缀匹配**：后缀 `^` → `^abc` 匹配以 “abc” 开头的行。
- **后缀匹配**：前缀 `$` → `abc$` 匹配以 “abc” 结尾的行。
- **正则表达式**：`!` 前缀用于反向匹配，或使用 `rg` 集成。

### 预览窗口
预览窗口显示高亮项的上下文信息。它可以使用外部命令，如 `cat`、`bat`、`head`，甚至自定义脚本：

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### Shell 集成
官方 `install` 脚本设置了三个便捷的快捷键（Bash、Zsh、Fish）：

| Shortcut | Action                |
|----------|-----------------------|
| `Ctrl+R` | 搜索命令历史           |
| `Ctrl+T` | 搜索文件/目录并粘贴其路径 |
| `Alt+C`  | 跳转到子目录（模糊 cd） |

### Vim / Neovim 插件
fzf 提供了一个原生 Vim 插件。最流行的扩展是 [fzf.vim](https://github.com/junegunn/fzf.vim)，它增加了如下命令：

| Command | Purpose |
|---------|---------|
| `:Files [path]` | 搜索文件 |
| `:Rg [pattern]` | 搜索文件内容（需要 ripgrep） |
| `:Buffers` | 切换打开的缓冲区 |
| `:GFiles?` | 搜索 Git 仓库中未跟踪的文件 |
| `:Commands` | 列出 Vim 命令 |
| `:Maps` | 显示键映射 |

### 可扩展性
由于 fzf 在 stdin/stdout 上运行，它可以无缝集成到任何工作流中。您可以将其封装在 Shell 函数或脚本中，创建自己的交互式菜单。

---

## 高级用例

### 进程终止器
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### 切换 Git 分支
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### 从配置 SSH 到主机
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### 带预览搜索文件内容
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### 交互式切换目录（使用 fd）
```bash
cd "$(fd --type d | fzf)"
```
或使用内置的 `Alt+C` 快捷键。

### Docker 容器搜索
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## 技巧与提示

- **使用 `--header` 选项** 显示说明：
  ```bash
  fzf --header "Press Ctrl-R for history, Ctrl-T for files"
  ```
- **将选中的项存储在变量中** 以便批量操作。
- **添加彩色预览**，使用支持 ANSI 的 `bat` 或 `highlight`。
- **与 `tmux` 结合使用**，在单独的分屏中打开预览窗格。
- **通过 `FZF_DEFAULT_OPTS` 环境变量自定义配色方案**：
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## 结论

fzf 是交互式终端搜索的黄金标准工具。其模糊匹配、速度和可组合性使其成为命令行重度用户不可或缺的工具。无论您是在浏览文件、查找进程还是构建自定义工作流，fzf 都能将繁琐的查找任务转变为流畅、近乎神奇的体验。

完整文档请访问 [GitHub 仓库](https://github.com/junegunn/fzf)。