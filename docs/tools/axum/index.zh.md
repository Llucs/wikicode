---
title: Axum：高性能的 Rust Web 框架
description: Axum 是一个基于 Tokio、Hyper 和 Tower 构建的现代、易用的 Rust Web 框架。它强调模块化、最少的样板代码以及通过 Tower 服务无缝组合中间件。
created: 2026-07-22
tags:
  - Rust
  - Web 框架
  - Tokio
  - Hyper
  - Tower
status: draft
---

# Axum：高性能的 Rust Web 框架

Axum 是一个异步的 Rust Web 框架，设计用于快速、安全和易用。它基于 Hyper HTTP 服务器和 Tokio 异步运行时构建，因此常被用来构建现代 Web 应用程序。Axum 强调模块化、最少的样板代码以及通过 Tower 服务无缝组合中间件。

## 什么是 Axum？

Axum 是一个高性能的 Rust Web 框架，由 Tokio 团队支持。它结合了优雅的 API 设计和 Tower 中间件生态系统的全部功能。Axum 以简单、高效和灵活性著称，适用于从简单的 API 到复杂的无服务器函数等各种 Web 应用程序。

## 核心特性

- **异步处理**：使用 Rust 的 async/await 语法和 Tokio 运行时高效处理数千个并发连接。
- **路由和中间件**：简单直观的路由和中间件支持。
- **与其他库的集成**：Axum 与其他 Rust 库集成良好，提供灵活的开发环境。
- **HTTP/2 支持**：内置 HTTP/2 支持，提高性能和效率。
- **安全特性**：内置支持安全最佳实践，如 CSRF 保护和安全标头。
- **可定制性**：高度可定制，适用于从简单的 Web 应用程序到复杂的无服务器函数的各种需求。

## 历史

Axum 由 Warp Web 框架团队创建，Warp 是最流行的 Rust Web 框架之一。Warp 的开发者认为可以通过引入更多 Rust 语言特性和提升性能来改进框架。因此，Axum 在 2019 年诞生，旨在比 Warp 更现代、更高效。

## 使用场景

- **Web 应用程序**：构建稳健且高性能的 Web 应用程序。
- **API**：开发 RESTful API 和 GraphQL 服务。
- **无服务器函数**：为 AWS Lambda 或 Azure Functions 等云平台创建无服务器函数。
- **实时应用程序**：使用 WebSockets 等技术构建实时应用程序。

## 安装

要安装 Axum，首先需要在系统上安装 Rust。然后可以使用 Cargo，Rust 的包管理器，来创建一个新的 Axum 项目。以下是安装步骤：

```bash
# 创建一个新的 Rust 项目
cargo new my_axum_app

# 进入项目目录
cd my_axum_app

# 在 Cargo.toml 中添加 Axum 依赖
cargo add axum
```

## 基本用法

以下是一个简单的示例，帮助你开始使用 Axum：

1. **定义一个路由**：

   ```rust
   use axum::{routing::get, Router};

   async fn hello_world() -> &'static str {
       "Hello, World!"
   }

   #[tokio::main]
   async fn main() {
       let app = Router::new().route("/", get(hello_world));
       axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
           .serve(app.into_make_service())
           .await
           .unwrap();
   }
   ```

2. **运行应用程序**：

   ```bash
   cargo run
   ```

这将在 `http://0.0.0.0:3000` 启动一个服务器，当您导航到 `http://localhost:3000` 时，将显示 "Hello, World!"。

## 高级特性

Axum 提供了多个高级特性，例如：

- **状态管理**：使用 `State` 在路由之间共享数据。
- **Cookies 和会话**：管理用户会话和 Cookies。
- **表单处理**：解析和验证表单数据。
- **认证和授权**：使用内置支持的认证和授权构建安全应用程序。

## 获取帮助

要查看完整的示例和更高级的用法，可以查看由社区维护的展示项目或教程。您还可以在 Axum 仓库中找到示例和文档。

## 结论

Axum 是一个强大且灵活的 Rust Web 框架，提供了广泛的特性，适用于简单的和复杂的 Web 应用程序。它的异步性质和与现代 Rust 库的集成使它成为构建高性能和可扩展 Web 服务的优秀选择。

---