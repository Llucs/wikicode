---
title: DBGate
description: DBGate 是一款开源、跨平台、基于 Web 的数据库管理工具，支持 MySQL、PostgreSQL、SQL Server、MongoDB、SQLite 等多种数据库，为数据库管理和开发提供现代化界面。
created: 2026-06-20
tags:
  - database
  - open-source
  - web-based
  - tool
  - management
status: draft
---

# DBGate

DBGate 是一款开源（MIT）、基于 Web 的数据库管理工具，旨在成为 phpMyAdmin、Adminer、DBeaver 或 DataGrip 等经典工具的现代替代品。它采用 Node.js/Express 后端和 React 前端构建，提供简洁、现代化的用户界面，完全在 Web 浏览器中运行，因此跨平台且非常适合云、服务器和容器化环境。

## 为什么选择 DBGate？

传统的数据库客户端通常需要在操作系统上安装，导致团队和环境之间出现碎片化问题。DBGate 通过完全基于浏览器的方式解决了这一问题，让您可以：

- **远程管理数据库**，无需 SSH 隧道或本地客户端。
- **集成到 Docker 环境**，实现即时开发数据库访问。
- **共享连接和脚本**，通过集中式实例（带有认证）。
- **跨 Windows、macOS 和 Linux 无缝工作**，使用相同的 Web 界面。

## 主要特性

| 特性 | 描述 |
|---|---|
| 多数据库支持 | 同时连接到 MySQL、MariaDB、PostgreSQL、SQL Server、MongoDB、SQLite、CockroachDB、Amazon Redshift 和 Redis。 |
| 高级 SQL 编辑器 | 语法高亮、智能自动补全、多标签查询以及全面的查询历史。 |
| 架构/数据浏览器 | 浏览、创建、修改和删除数据库对象。内联数据编辑，支持强大的排序和过滤。 |
| ER 图 | 自动生成实体关系图以可视化数据库架构。 |
| 导出/导入 | 导出为 CSV、JSON、SQL、Markdown、Excel；从 CSV 和 SQL 文件导入。 |
| 外键导航 | 从数据浏览器直接深入相关记录。 |
| 服务器监控 | 查看活动进程、服务器状态和变量配置。 |
| Docker 优化 | 官方 Docker 镜像，方便在任何服务器上部署。 |
| 桌面应用 | 集成的 Electron 版本，可在 Windows、macOS 和 Linux 上独立使用。 |

## 安装

DBGate 可以通过多种方式安装和运行：

### 1. Docker（推荐用于服务器）

```bash
docker run -d -p 3000:3000 --name dbgate dbgate/dbgate
```

然后访问 `http://localhost:3000`。

对于 `docker-compose.yml` 配置：

```yaml
version: '3'
services:
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    restart: unless-stopped
```

### 2. Node 包管理器 (NPM)

```bash
npm install -g dbgate
dbgate
```

通过 `http://localhost:3000` 访问。

### 3. 桌面安装程序

从 [GitHub 发布页面](https://github.com/dbgate/dbgate/releases) 下载适用于 Windows、macOS 和 Linux 的预构建安装程序。

### 4. 云部署

提供适用于 Heroku、Railway 及类似平台的一键部署选项。

## 快速入门 / 使用方法

### 1. 启动 DBGate

在浏览器中导航到 `http://localhost:3000`。

### 2. 添加连接

点击 **连接** 旁边的 **+** 图标。选择您的数据库引擎（例如 PostgreSQL），然后输入连接凭据：主机、端口、用户名、密码、数据库。

### 3. 浏览数据

点击已保存的连接以查看数据库/表的树状结构。点击某个表即可查看其行数据。

### 4. 查询数据库

点击 **查询** 按钮打开 SQL 编辑器。编写 SQL 语句并点击 **执行**（或 `Ctrl+Enter`）。

### 5. 可视化架构

右键点击数据库或表，然后选择 **ER 图** 以生成可视化架构。

### 6. 导出数据

右键点击表或结果集，然后选择 **导出** 以下载所需格式（CSV、JSON、SQL 等）的数据。

## 命令示例

**使用 Docker 启动 DBGate 并持久化数据：**

```bash
docker run -d \
  -p 3000:3000 \
  -v dbgate-data:/home/app/.dbgate \
  --name dbgate \
  dbgate/dbgate
```

**在开发环境栈中使用本地 PostgreSQL 实例：**

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    depends_on:
      - postgres
```

**使用 npm 安装和运行：**

```bash
npm install -g dbgate
dbgate
```

**使用环境变量连接（高级）：**

```bash
docker run -d \
  -e DBGATE_SERVER_NAME=myPostgres \
  -e DBGATE_SERVER_TYPE=postgres \
  -e DBGATE_SERVER_HOST=192.168.1.100 \
  -e DBGATE_SERVER_PORT=5432 \
  -e DBGATE_SERVER_USER=admin \
  -e DBGATE_SERVER_PASSWORD=secret \
  -p 3000:3000 \
  dbgate/dbgate
```

## 使用场景

1. **远程服务器管理** – 无需 SSH 隧道或安装本地客户端，即可管理 VPS 或云实例上的数据库。
2. **开发环境** – 将 DBGate 包含在 `docker-compose.yml` 栈中，让开发人员即时通过 GUI 访问其本地数据库。
3. **团队工具** – 部署集中式 DBGate 实例（带有适当认证），以便团队共享对开发或预发布数据库的访问。
4. **教育与培训** – 无需管理客户端安装，即可快速为学生提供 SQL 界面。
5. **跨平台工作流** – 使用相同的 Web 界面在不同操作系统之间无缝切换。

## 架构

DBGate 包含：

- **后端：** Node.js/Express 服务器，处理数据库连接、查询执行和 API 端点。
- **前端：** 基于 React 的 SPA（单页应用），提供用户界面，包括 SQL 编辑器、数据浏览器和架构查看器。
- **数据库驱动：** 通过原生 Node.js 驱动或 ODBC/JDBC 桥接器支持多种数据库引擎。

应用程序将连接、SQL 脚本和其他对象存储在本地存储中（或托管版本的可选云存储）。Docker 镜像捆绑了所有依赖项，实现单端口部署。

## 局限性

- **高级 IDE 功能：** 可能缺少 IntelliJ DataGrip 中的某些功能（例如分布式重构、高级代码分析）。
- **性能：** 在浏览器中渲染非常大的数据集（>10 万行）可能比原生应用慢。导出操作在服务器端处理以提高性能。
- **身份验证：** 开源版本不包含内置用户身份验证；团队使用时必须使用反向代理（如 nginx + auth_basic）进行保护。

## 总结

DBGate 是一款强大、灵活且开源的数据库管理工具，填补了轻量级 Web 客户端（如 phpMyAdmin）和重型原生 IDE（如 DataGrip）之间的空白。其跨平台特性、友好的容器设计以及不断增长的功能集，使其成为开发者、DBA 和团队寻找现代化 Web 原生数据库客户端的绝佳选择。

---

*文档生成于 2026-06-20。请访问[官方仓库](https://github.com/dbgate/dbgate)获取最新更新。*