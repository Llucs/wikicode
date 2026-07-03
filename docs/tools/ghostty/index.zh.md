---
title: Ghostty - 一个快速且功能丰富的终端模拟器
description:  Ghostty 是一个快速、功能丰富且跨平台的终端模拟器，使用平台原生界面和 GPU 加速。
created: 2026-07-03
tags:
  - 终端
  - 模拟器
  - 生产力
  - 命令行
  - 跨平台
status: 草稿
---

# Ghostty - 一个快速且功能丰富的终端模拟器

Ghostty 是一个快速、功能丰富且跨平台的终端模拟器，使用平台原生界面和 GPU 加速。它旨在成为 macOS 和 Linux 上当前终端模拟器的最佳替代品。Ghostty 由 Mitchell Hashimoto 开发，他是 HashiCorp 的联合创始人，其目标是在 2026 年成为新的性能标准。

## 什么是 Ghostty？

Ghostty 不是一个用于生成项目或搭建应用程序的工具，而是一个提供现代高效用户界面的终端模拟器。它提供快速且响应迅速的体验，带有 GPU 加速和原生界面，对于希望在终端环境中提升生产力的开发人员来说是一个更优的选择。

## 核心功能

- **平台原生界面**：提供现代且直观的用户界面。
- **GPU 加速**：增强性能和响应速度。
- **跨平台支持**：在 macOS、Linux 和 Windows 上无缝工作。
- **快速**：即使处理复杂的命令和大规模文件操作也提供闪电般的性能。
- **功能丰富**：包括多标签终端、多个分屏等高级功能。

## 历史

Ghostty 由 Ghost 项目团队开发，该团队致力于简化内容管理系统和 Web 应用程序的构建过程。Mitchell Hashimoto，前 HashiCorp 的 CEO 和 CTO，是 Ghostty 的主要开发者，致力于提升终端模拟器的体验。

## 使用案例

Ghostty 主要用于与命令行工具交互、管理进程和执行脚本的终端环境中。对于需要快速且高效终端模拟器的开发人员和系统管理员来说，它尤其有用。

## 安装

要安装 Ghostty，请按照以下步骤操作：

1. **安装 Node.js**：确保您的系统上已安装 Node.js。Ghostty 使用 Node.js 构建。
2. **安装 Ghostty**：在您的终端中运行以下命令：

   ```sh
   npm install -g ghostty
   ```

   或者，您可以通过 Yarn 安装：

   ```sh
   yarn global add ghostty
   ```

## 基本用法

安装完成后，您可以使用 Ghostty 与终端进行交互。这里是一些基本命令：

1. **启动 Ghostty**：通过运行以下命令打开 Ghostty：

   ```sh
   ghostty
   ```

2. **打开新终端**：在 Ghostty 中打开一个新的终端窗口：

   ```sh
   ghostty new-terminal
   ```

3. **关闭当前终端**：退出当前终端窗口：

   ```sh
   ghostty close-terminal
   ```

4. **在终端间切换**：使用 Tab 键在打开的终端间切换：

   ```sh
   ghostty switch-terminal
   ```

5. **打开文件**：在终端中打开文件：

   ```sh
   ghostty open-file /path/to/file.txt
   ```

6. **在终端中运行命令**：在终端中执行命令：

   ```sh
   ghostty run-command ls -l
   ```

7. **关闭 Ghostty**：通过按下 Ctrl + D 或运行以下命令退出 Ghostty：

   ```sh
   ghostty exit
   ```

## 结论

Ghostty 是一个强大且高效的终端模拟器，提供现代且响应迅速的用户界面。它旨在提升您在终端环境中的生产力，并且对于寻求快速且功能丰富终端模拟器的开发人员和系统管理员来说是一个值得的选择。

如需更多资讯和探索其他功能，请访问 [官方 Ghostty GitHub 仓库](https://github.com/mitchellh/ghostty)。