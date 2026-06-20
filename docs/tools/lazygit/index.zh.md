---
title: Lazygit – 提升生产力的终端 Git UI
description: 全面指南：lazygit 是一个基于终端的 Git UI，通过直观的键盘驱动界面，简化了暂存、变基和冲突解决等复杂 Git 操作。
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – 提升生产力的终端 Git UI

**Lazygit** 是一个跨平台、键盘驱动的终端用户界面（TUI），专为 Git 打造。由 Jesse Duffield 于 2018 年创建，采用 Go 语言编写，它将 Git 最复杂且容易出错的操作包装到一个直观的、基于面板的布局中，完全运行在你的终端内。

> “别再死记 Git 命令。开始直观地使用 Git。”

---

## 为什么选择 Lazygit？

Git 的命令行界面虽然强大，但众所周难以驾驭。交互式变基（interactive rebase）、暂存区块（staging hunks）、解决冲突和管理分支都需要精确的命令序列。Lazygit 通过以下方式解决这些问题：

- **可视化你的仓库** – 一眼查看 branches、tags、commit graph、working tree 和 stash。
- **加速日常工作** – 无需输入任何 `git` 命令即可 stage、commit、push 和 pull。
- **减少错误** – interactive rebasing、cherry-picking 和 conflict resolution 变得菜单驱动且可撤销。
- **降低学习曲线** – 新团队成员可以立即执行高级 Git 操作，无需记忆晦涩的语法。
- **跨平台运行** – 在 Linux、macOS 和 Windows 上以相同的界面和按键绑定工作。

---

## 安装

Lazygit 可通过多数包管理器安装。选择你的平台：

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

## 基本用法

进入任意 Git 仓库后启动：

```bash
cd my-project
lazygit
```

Lazygit 打开后呈现分割面板布局。左侧列从上到下显示 **Status**、**Files**、**Branches**、**Commits** 和 **Stash** 面板。右侧显示选中项目的 diff 或日志。

### 面板导航

| 按键 | 动作 |
|------|------|
| `←` / `→` | 在面板之间移动 |
| `Tab` | 向前循环切换面板 |
| `Shift + Tab` | 向后循环切换面板 |
| `j` / `k` | 在面板内上下移动 |
| `J` / `K` | 滚动主 diff 面板 |
| `?` | 显示/隐藏完整的按键绑定帮助 |

### 快速入门（日常工作流程）

1. **启动** – 在仓库内运行 `lazygit`。
2. **暂存文件** – 在 Files 面板中对文件按 `Space`。
3. **暂存特定区块** – 按 `Enter` 查看 diff，再对个别 hunks 按 `Space`。
4. **提交** – 按 `c`，输入提交信息，再按 `Enter`。
5. **推送** – 按大写 `P` 进行 push。
6. **拉取** – 按小写 `p` 进行 pull。
7. **退出** – 按 `q` 退出。

---

## 主要特性（含命令示例）

### 🎯 交互式暂存（优于 `git add -p`）

查看文件的 diff，然后可视化地暂存/取消暂存个别行或区块。无需再手动数光标位置。

```bash
# 在 Files 面板内：
# Enter  → 打开文件 diff
# Space  → 暂存选中的 hunk
# a      → 暂存所有更改
# 在特定 hunk 上按 Enter → 暂存个别行
```

### 🔁 交互式变基（杀手级功能）

通过单次按键即可重排、合并、修复、编辑或删除 commits。

```bash
# 切换到 Commits 面板（按 4）：
# i       → 启动 interactive rebase
# s       → squash commit 到前一个
# f       → fixup（squash，丢弃 commit 信息）
# d       → 完全删除 commit
# e       → 编辑 commit（暂停 rebase）
# r       → 重写 commit 信息
# Ctrl+j  → 向下移动 commit
# Ctrl+k  → 向上移动 commit
```

标记完成后，按 `Enter` 确认。Lazygit 执行变基并显示进度。如果出现冲突，会自动跳转到冲突解决面板。

### ↩️ 撤销 / 重做（安全网）

Lazygit 会记录自己的内部操作历史。在变基中犯了错或不小心删除了 commit？一键撤销。

```bash
# z  → 撤销上一次操作
# Z (Shift+z)  → 重做
```

### 🌳 分支管理

无需离开 UI 即可切换、合并、变基、重命名和删除分支。

```bash
# 按 3 进入 Branches 面板：
# Space    → checkout 选中的分支
# n        → 创建新分支（可选择基于当前 HEAD）
# m        → 将选中的分支合并到当前分支
# r        → 将当前分支变基到选中的分支上
# R        → 重命名分支
# d        → 删除分支（需要确认）
# Ctrl+r   → 更新远程分支引用
```

### 🍒 Cherry-Pick Commits

无需使用 `git log` 或搜索 commit hash，即可将 commits 从一个分支复制到另一个分支。

```bash
# 在 Commits 面板中：
# c        → 启动 cherry-pick 模式
# Space    → 切换选中一个 commit
# Shift+c  → 完成 cherry-pick
```

### 🧩 Stash 管理

为 stash 命名、应用、弹出，甚至从 stash 创建分支。

```bash
# 按 5 进入 Stash 面板：
# g        → 切换 stash 视图
# s        → stash 已暂存的更改
# Shift+s  → stash 所有更改（包括未跟踪文件）
# Space    → 应用选中的 stash
# d        → 删除 stash
# n        → 为新 stash 命名
# b        → 从 stash 创建分支
```

### ⚔️ 冲突解决

当变基或合并产生冲突时，Lazygit 会显示带有内联冲突标记的三路 diff。可视化地解决它们。

```bash
# 冲突面板会自动打开：
# Ctrl+o → 在外部合并工具中打开文件
# Space  → 暂存已解决的文件
# Enter  → 手动编辑文件
# /      → 搜索剩余的冲突标记
```

### 🌳 Worktree 支持

Lazygit 原生支持 Git worktrees，可轻松添加、删除和切换它们。

```bash
# 在 Branches 面板（或专门的 Worktrees 面板）中：
# w        → 打开 worktree 管理
# a        → 添加新的 worktree
# d        → 删除 worktree
# Space    → 切换到一个 worktree
```

### 🧹 自定义命令

通过自己的 shell 命令或脚本扩展 Lazygit，这些命令会出现在 UI 中。

```bash
# 在 ~/.config/lazygit/config.yml 中：
customCommands:
  - key: "C"
    command: "git cz"
    description: "用 Commitizen 提交"
    context: "files"
    loadingText: "正在打开 commitizen..."
```

---

## 专业技巧

1. **接近 Vim 的按键绑定** – `j/k` 导航，`J/K` 滚动 diff，`/` 在面板内搜索。
2. **过滤文件** – 在 Files 面板中按 `/` 并输入文件名进行过滤。
3. **与特定 commit 对比** – 在 Commits 面板中对某个 commit 按 `d`，查看该 commit 的改动。
4. **切换 diff 可见性** – 按 `Ctrl+d` 在 diff 显示模式间循环。
5. **与现有 Git 配置一起使用** – Lazygit 会尊重你的别名、difftool 和 merge tool 设置。

---

## 配置

Lazygit 高度可配置。完整的配置文件位于：

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

使用以下命令生成模板：

```bash
lazygit --print-config
```

常见设置包括重写按键绑定、主题颜色、自定义命令和 UI 布局。

---

## 何时使用 Lazygit

| 场景 | Lazygit 的优势 |
|------|----------------|
| 交互式变基 | 可视化选择并重排 commits；可撤销 |
| 暂存部分更改 | 逐行选择 hunks，即时显示 diff |
| 新手上路 | 无需记忆复杂 Git 命令 |
| 代码审查准备 | 数分钟内创建干净、逻辑清晰的 commit 序列 |
| 冲突解决 | 三路 diff 查看器，附带内联操作 |
| 仓库概览 | 一眼查看 branches、tags、remotes、stash 和 commit graph |

---

## 资源

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **文档:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **配置参考:** [lazygit Configuration](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **作者的 “lazy” 生态系统:** Lazygit、Lazydocker、Lazynpm – 都遵循相同的 TUI 哲学。

---

Lazygit 并不替代 Git；它让 Git 变得触手可及、可视化且高效。无论你是经验丰富的 Git 高手，还是只想尽快回到写代码状态的开发者，Lazygit 每周都能为你节省数小时的时间。给自己一天时间试试，你将再也不愿回到那个只靠 `git rebase -i` 的纯命令行时代了。