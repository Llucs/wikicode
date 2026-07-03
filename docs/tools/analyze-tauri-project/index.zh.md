---
title: Tauri 开发者指南
description: 一个使用网页技术构建原生图形用户界面（GUI）应用的框架的全面指南。
created: 2026-07-03
tags:
  - 开发工具
  - 网页开发
  - Rust
  - tauri
status: 草稿
---

# Tauri 开发者指南

## 什么是 Tauri？

Tauri 是一个开源框架，用于使用网页技术（HTML、CSS、JavaScript）构建原生用户界面（UI）。它结合了现代网页运行时技术（如 WebAssembly），使开发者能够使用网页技术创建桌面应用程序，而无需受到网页浏览器的限制，提供原生体验。

### 核心功能

1. **网页技术**：前端使用网页技术（HTML、CSS、JavaScript）。
2. **WebAssembly**：可以直接在应用程序中运行 WebAssembly，卸载 CPU 密集型任务。
3. **原生集成**：提供了文件访问、剪贴板、系统托盘等原生系统 API。
4. **性能**：经过优化，旨在与原生应用程序一样快速。
5. **跨平台**：在 Windows、macOS 和 Linux 上运行。
6. **零配置构建**：简化构建过程，使用零配置构建系统。
7. **自定义**：高度可定制，具有插件系统和内置支持各种 UI 框架，如 GTK、Qt 等。
8. **安全性**：设计时考虑安全性，具有沙箱功能和模块化架构。

## 历史

Tauri 由 OpenJS 基金会 OpenJS 基金会桌面项目的团队开发。该项目旨在解决使用网页技术构建跨平台桌面应用程序的更高效和更安全的方法。该项目获得了显着的关注和支持，导致它从 OpenJS 基金会桌面项目分离并成为一个独立的开源项目。

## 使用场景

- **生产力工具**：如文本编辑器、代码编辑器和项目管理工具。
- **媒体播放器**：如音乐播放器、视频播放器和其他与媒体相关的应用程序。
- **实用工具**：如文件管理器、系统监视器和其他系统实用工具。
- **游戏**：需要原生体验的简单和中型游戏。
- **企业应用程序**：为企业使用的定制桌面应用程序。

## 安装

要开始使用 Tauri，您需要在系统上安装 Rust 和 Cargo。以下是设置 Tauri 项目的步骤：

1. **安装 Rust 和 Cargo**：遵循官方 Rust 文档安装 Rust 和 Cargo。
2. **安装 Tauri CLI**：将 Tauri CLI 添加到 PATH。
3. **创建一个新的 Tauri 项目**：
   ```bash
   cargo tauri init
   ```
   该命令将创建一个带有基本设置的新 Tauri 项目。
4. **构建和运行**：
   ```bash
   cargo tauri build
   cargo tauri dev
   ```

## 基本用法

1. **网页应用程序**：Tauri 应用程序的核心是一个使用 HTML、CSS 和 JavaScript 构建的网页应用程序。该应用程序由 Tauri 运行时提供服务。
2. **UI 框架**：Tauri 支持各种 UI 框架，如 GTK、Qt 和 Sycosis。您可以选择最适合您需求的框架。
3. **系统 API**：使用 Tauri 提供的 API 与系统进行交互。例如，访问文件系统：
   ```rust
   use tauri::api::fs::{read_dir, read_file, write_file};

   tauri::command!(async fn read_file_command(path: String) -> Result<String, String>) {
       let content = read_file(path).await.map_err(|err| err.to_string())?;
       Ok(content)
   }
   ```
4. **WebAssembly**：可以集成 WebAssembly 模块以卸载繁重的计算。
5. **部署**：Tauri 提供了打包和部署应用程序到不同平台的工具。

## 结论

Tauri 提供了一个使用网页技术构建原生桌面应用程序的强大且灵活的框架。其结合的性能、跨平台支持和丰富的功能使其成为开发人员构建高效和安全的桌面应用程序的优秀选择。