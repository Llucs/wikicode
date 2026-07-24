---
title: DBeaver 社区版
description: 一个推荐用于个人项目的免费开源数据库管理工具。管理和探索 MySQL、MariaDB、PostgreSQL、SQLite、Apache 系列以及其他 SQL 数据库。
created: 2026-07-24
tags:
  - database
  - sql
  - management
  - development
  - tool
status: draft
---

# DBeaver 社区版

DBeaver 是一个支持多种数据库的开源通用数据库管理工具，包括 SQL Server、MySQL、PostgreSQL、Oracle、SQLite 等。它最初于 2013 年发布，并已成为开发人员、数据库管理员和数据分析师进行数据库管理、开发和管理的热门选择。

## 关键功能

1. **数据库管理**：DBeaver 支持多种数据库及其相应工具，如 SQL 查询编辑器、数据库浏览器、模式编辑器和 SQL 历史记录。
2. **数据建模和设计**：DBeaver 通过图形用户界面允许用户设计、管理和修改数据库模式。
3. **数据库连接**：使用不同的协议和驱动程序连接到各种数据库。
4. **SQL 编辑器**：SQL 编辑器功能包括语法高亮、代码完成和自动完成助手。
5. **数据导出和导入**：DBeaver 提供了将数据导出到 CSV、Excel 等格式以及从这些格式导入数据的工具。
6. **数据库同步**：支持同步和比较数据库模式。
7. **数据库管理**：DBeaver 包括管理用户、角色、权限和其他管理任务的功能。
8. **图形用户界面**：应用程序具有现代、直观的界面，支持深色和浅色主题。
9. **插件和扩展**：用户可以通过插件扩展 DBeaver 的功能，这些插件可以从 DBeaver 市场中安装。

## 历史

DBeaver 初始由 Yvan Volckaert 开发，并于 2013 年作为社区项目发布。该项目后来被 DBeaver 社区采用和维护。2017 年，该项目转变为商业公司 DBeaver GmbH，继续支持和发展该软件。

## 使用案例

1. **数据库开发**：开发人员可以使用 DBeaver 编写、测试和执行 SQL 查询，以及管理数据库模式。
2. **数据分析**：数据分析师可以使用 DBeaver 查询和操作大量数据集，创建并运行复杂的 SQL 查询，并生成报表。
3. **数据库管理**：数据库管理员可以使用 DBeaver 管理用户权限、角色和其他管理任务。
4. **数据迁移**：用户可以使用 DBeaver 在不同数据库之间迁移数据，尤其是当目标数据库结构不同时。

## 安装

1. **下载**：访问官方网站（https://dbeaver.io/）下载最新版本的 DBeaver。
2. **安装**：安装过程非常简单。对于 Windows，双击安装程序并按照屏幕上的指示操作。对于 macOS，打开 `.dmg` 文件并将应用程序拖放到应用程序文件夹。对于 Linux，使用包管理器运行 `.deb` 或 `.rpm` 文件。
3. **运行**：安装完成后，从应用程序菜单中打开 DBeaver。

### 示例命令用于 Windows 安装程序

```sh
sh DBeaver-<version>-win32-installer.exe
```

### 示例命令用于 macOS 安装程序

```sh
open DBeaver-<version>-macOS.dmg
```

### 示例命令用于 Linux 安装程序

```sh
sudo dpkg -i DBeaver-<version>.deb
```

或

```sh
sudo rpm -i DBeaver-<version>.rpm
```

## 基本用法

1. **连接管理**：打开 DBeaver，点击 "文件" > "新建" > "数据库连接"，并配置数据库连接设置（服务器、端口、用户名、密码）。
2. **SQL 编辑器**：连接后，使用 SQL 编辑器编写、执行和管理 SQL 查询。
3. **模式浏览器**：使用模式浏览器探索数据库结构，导航表、视图和其他数据库对象。
4. **数据导入/导出**：利用导入和导出功能在不同格式或数据库之间移动数据。

## 命令行界面 (dbvr)

DBeaver CLI (dbvr) 是一个用于处理数据库的命令行界面。它可以作为独立的 CLI 应用程序或与 DBeaver 和 CloudBeaver 结合使用。它提供了从终端管理数据库项目和数据源、检查元数据和执行 SQL 的脚本化方式。

### 示例命令连接到数据库

```sh
dbvr connect --url jdbc:mysql://localhost:3306/mydb --username myuser --password mypassword
```

### 示例命令执行 SQL 查询

```sh
dbvr sql -c "SELECT * FROM mytable" -o results.csv
```

## 结论

DBeaver 是一个强大且多功能的工具，提供了广泛的数据库管理和开发功能。其开源性质和活跃的社区使其具有强大的功能和频繁的更新，成为数据库专业人士的重要资源。