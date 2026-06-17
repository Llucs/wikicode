---
title: Git - 版本控制系统
description: Git 是一个分布式版本控制系统，用于在软件开发项目中跟踪源代码的变更。
created: 2026-06-13
tags:
  - Source_Control
  - Versioning
status: draft
ecosystem: vcs
---

Git 是一个强大且广泛使用的分布式版本控制系统（VCS），旨在快速高效地处理从小型到超大型项目的所有事务。它由 Linus Torvalds 于 2005 年为 Linux 内核开发团队创建，但此后已成为管理软件代码变更的行业标准工具。

### 什么是 Git？

Git 是一个版本控制系统，允许开发者随时间跟踪文件的变化、与他人协作项目，并在必要时恢复到以前的版本。它采用“分布式”模型，每个开发者都有自己的仓库副本，可以与其他仓库推送和拉取变更。

### 为什么使用 Git？

1. **速度**：Git 针对速度和效率进行了优化，使其适用于大型项目。
2. **灵活性**：凭借其分布式特性，Git 允许开发者独立工作，同时仍保持项目开发的共享历史。
3. **功能丰富**：它支持如分支和合并等复杂工作流，以及子模块和钩子等高级功能。

### 安装 Git

要在你的系统上安装 Git：

- **Windows**：从 Git 官方网站下载安装程序并按照安装说明操作。
- **macOS**：使用 Homebrew 安装 Git：`brew install git`。
- **Linux**：大多数 Linux 发行版的包管理器中都包含 Git。例如，在 Ubuntu 上，可以使用 `sudo apt-get install git`。

### 基本用法

以下是一些入门的基本命令：

```sh
# Initialize a new repository (create .git directory)
git init

# Add files to staging area
git add filename.txt

# Commit changes with message
git commit -m "Initial commit"

# View the list of untracked files
git status

# Create a new branch and switch to it
git checkout -b feature-branch

# Merge changes from another branch into your current branch
git merge other-branch

# Push local commits to remote repository (e.g., GitHub)
git push origin main
```

### 主要功能

Git 提供了几个使其成为软件开发重要工具的功能：

1. **分支与合并**：轻松创建分支，独立在其上工作，然后将更改合并回原始分支。
2. **子模块**：允许你将其他 Git 仓库作为项目依赖项的一部分包含进来。
3. **钩子**：在 Git 操作的不同时间点运行的自定义脚本（例如，pre-commit 钩子）。
4. **引用日志**：提供在仓库中执行的所有命令的记录，对于故障排除很有用。

### 结论

Git 是一个强大且灵活的版本控制系统，已成为许多软件开发团队不可或缺的工具。其强大的功能，加上效率和灵活性，使其成为跨项目管理源代码变更的绝佳选择。

有关 Git 用法和最佳实践的更多详细信息，请参考 Git 官方文档或在线资源。