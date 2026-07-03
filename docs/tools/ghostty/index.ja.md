---
title: Ghostty - 速くて機能豊かなターミナルエミュレーター
description: Ghosttyは、プラットフォーム固有のUIとGPU加速を用いた、高速で機能豊かなクロスプラットフォームのターミナルエミュレーターです。
created: 2026-07-03
tags:
  - ターミナル
  - エミュレーター
  - 生産性向上
  - コマンドライン
  - クロスプラットフォーム
status: 草稿
---

# Ghostty - 速くて機能豊かなターミナルエミュレーター

Ghosttyは、プラットフォーム固有のUIとGPU加速を利用した、高速で機能豊かなクロスプラットフォームのターミナルエミュレーターです。macOSやLinuxで現在使用中のターミナルエミュレーターの代わりになる最高の代替品として設計されています。GhosttyはMitchell Hashimotoによって開発され、2026年の新規性能基準を目指しています。Mitchell HashimotoはHashiCorpの共同創業者であり、クラウドインフラストラクチャの構築と管理を行う企業です。

## 什么是Ghostty？

Ghostty不是用于生成项目或创建应用程序骨架的工具，而是一个提供现代化且高效的用户界面的终端仿真器。它提供快速且响应迅速的体验，具有GPU加速和原生UI，使其成为在终端环境中提高生产力的理想选择。

## 主要功能

- **原生UI**：提供现代化且直观的用户界面。
- **GPU加速**：提高性能和响应速度。
- **跨平台支持**：无缝运行于macOS、Linux和Windows。
- **快速**：即使处理复杂命令和大量文件操作也能提供闪电般的速度。
- **功能丰富**：包括标签页终端、多个分屏等高级功能。

## 历史

Ghostty由Ghost Project团队开发，旨在简化内容管理系统和Web应用程序的构建过程。Mitchell Hashimoto是前HashiCorp的CEO和CTO，是Ghostty的主要开发者，致力于提升终端仿真器的使用体验。

## 使用案例

Ghostty主要用于终端环境中与命令行工具进行交互、管理进程和执行脚本。对于需要快速且高效终端仿真器的开发者和系统管理员来说，Ghostty特别有用。

## 安装

要安装Ghostty，请按照以下步骤操作：

1. **安装Node.js**：确保系统上已安装Node.js。Ghostty是基于Node.js构建的。
2. **安装Ghostty**：打开终端并运行以下命令：

   ```sh
   npm install -g ghostty
   ```

   或者，您可以通过Yarn安装：

   ```sh
   yarn global add ghostty
   ```

## 基本用法

安装后，您可以使用Ghostty与终端进行交互。以下是基本命令：

1. **启动Ghostty**：通过运行以下命令来打开Ghostty：

   ```sh
   ghostty
   ```

2. **打开一个新的终端**：在Ghostty中打开一个新的终端窗口：

   ```sh
   ghostty new-terminal
   ```

3. **关闭当前终端**：退出当前终端窗口：

   ```sh
   ghostty close-terminal
   ```

4. **在终端之间切换**：使用Tab键在打开的终端之间切换：

   ```sh
   ghostty switch-terminal
   ```

5. **打开一个文件**：在终端中打开一个文件：

   ```sh
   ghostty open-file /path/to/file.txt
   ```

6. **在终端中执行命令**：在终端中执行命令：

   ```sh
   ghostty run-command ls -l
   ```

7. **关闭Ghostty**：通过按Ctrl + D或运行以下命令来退出Ghostty：

   ```sh
   ghostty exit
   ```

## 结论

Ghostty是一个功能强大且高效的终端仿真器，提供现代化且响应迅速的用户界面。它旨在增强在终端环境中的生产力，并且是开发人员和系统管理员值得选择的快速且功能丰富的终端仿真器。

要获取更多信息并探索更多功能，请访问[官方Ghostty GitHub仓库](https://github.com/mitchellh/ghostty)。