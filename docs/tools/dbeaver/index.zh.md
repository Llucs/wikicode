---
title: DBeaver - 通用数据库管理工具
description: 一款免费、开源、跨平台的数据库管理工具和SQL客户端，适用于开发人员、DBA和数据分析师。
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - 通用数据库管理工具

## 概述

DBeaver 是一款**免费、开源、跨平台**的数据库管理工具和SQL客户端。它提供丰富的图形界面，可与任何支持JDBC或ODBC驱动的数据库交互，成为开发人员、数据库管理员和数据分析师的全能工具。

- **许可证**：社区版 (CE) 基于 **Apache 2.0** 发布；同时提供商业版 Pro/Enterprise/Team。
- **平台**：Windows、macOS、Linux（也提供便携版）。
- **架构**：基于 Eclipse Rich Client Platform (RCP) 构建，使用 Java。
- **历史**：2010 年由 Serge Rielau 发起，他曾参与 Apache Derby 和 Oracle 项目。该工具迅速获得广泛采用，并促成了 DBeaver Corp. 的成立。

DBeaver 适用于：
- **应用程序开发** – 编写、调试和优化SQL查询。
- **数据库管理** – 管理模式、用户、会话和索引。
- **数据分析** – 运行分析查询并将结果导出为多种格式。
- **数据工程** – 在不同数据库之间传输数据，无需大量脚本。
- **教育** – 通过直观的GUI学习SQL和关系数据库概念。

## 主要特性

| 特性 | 描述 |
|---------|-------------|
| **广泛的数据库支持** | 开箱即用，可连接100多种数据库，包括 MySQL/MariaDB、PostgreSQL、Oracle、SQL Server、SQLite、DB2、Snowflake、Redshift、ClickHouse 等。 |
| **高级SQL编辑器** | 语法高亮、代码补全、多结果标签页查询执行、执行计划可视化（图形化）、SQL格式化和参数化查询。 |
| **数据浏览器/电子表格** | 强大的内联编辑、高级过滤、排序，直接在网格界面中处理 BLOB/CLOB 数据。 |
| **ER图** | 自动生成实体关系图，支持逆向工程（右键单击模式或表）。 |
| **模式管理** | 对象浏览器，用于浏览、创建和编辑表、视图、索引、过程和函数。 |
| **数据传输** | 在数据库和文件格式（CSV、JSON、XML、Excel、SQL、Markdown、HTML）之间批量导出/导入。 |
| **管理工具** | 会话管理器、任务调度器 (Pro)、用户/角色管理，以及集成 SSH/SSL/代理隧道。 |
| **可扩展性** | 插件架构；提供用于额外驱动、版本控制 (Git) 和图表自定义的插件。 |
| **跨平台** | 支持 Windows、macOS 和 Linux。 |

## 安装

DBeaver 可通过多种渠道获取。选择适合您环境的方式。

### 官方安装程序（所有平台）

从 [dbeaver.io](https://dbeaver.io)（社区版）或 [dbeaver.com](https://dbeaver.com)（企业版）下载适用于您操作系统的安装程序。

### 包管理器

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – Official Debian/RPM repos)**
```bash
# Debian/Ubuntu
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt update && sudo apt install dbeaver-ce

# RHEL/CentOS/Fedora
sudo rpm --import https://dbeaver.io/rpms/dbeaver.gpg.key
sudo yum install dbeaver-ce
```

**Windows (winget / Chocolatey)**
```powershell
# winget (Windows 10 / 11)
winget install DBeaver.DBeaverCE

# Chocolatey
choco install dbeaver
```

**Windows 便携版**

官方提供便携式可执行文件，适合从USB驱动器运行，无需安装。

## 快速入门 - 基本使用

### 1. 创建数据库连接

1. 启动 DBeaver。
2. 点击工具栏中的**新建数据库连接**按钮（插头图标）。
3. 选择您的数据库类型（例如 **PostgreSQL**）。
4. 填写连接详情：
   - 主机、端口、数据库名称、用户名、密码。
5. 点击**测试连接**。如果未缓存，DBeaver 会自动提示下载所需的 JDBC 驱动。
6. 点击**完成**。连接将出现在**数据库导航器**面板中。

![连接向导示例](https://dbeaver.com/docs/images/connection-wizard.png)

### 2. 浏览和查询数据

- 在**数据库导航器**中，展开连接以查看模式、表、视图等。
- 右键单击表并选择**查看数据**以打开数据网格。
- 要编写自定义 SQL，请按 `Ctrl + ]`（Windows/Linux）或 `Cmd + ]`（macOS）打开新的**SQL编辑器**。

**示例 SQL 查询：**
```sql
-- Select users with their latest order
SELECT u.id, u.name, o.order_date
FROM users u
JOIN (
    SELECT user_id, MAX(order_date) AS order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
ORDER BY o.order_date DESC;
```

- 使用 `Ctrl + Enter`（Windows/Linux）或 `Cmd + Enter`（macOS）执行查询。
- 结果出现在编辑器下方的结果网格中。

### 3. 编辑和导出数据

- 直接单击结果网格中的单元格值进行编辑（需要表的**编辑**权限）。
- 右键单击结果网格并选择**导出数据**。
- 选择所需格式（CSV、Excel、JSON、SQL INSERT、XML、Markdown 等）并配置选项。

## 高级用法

### 实体关系 (ER) 图

DBeaver 可以为模式或特定表生成 ER 图。

1. 在数据库导航器中右键单击模式。
2. 选择**查看关系图**（或打开**ER图**选项卡）。
3. 关系图显示表、列、关系和索引。
4. 您可以重新排列元素，将关系图导出为图像或打印。

### 数据传输/迁移

使用**数据传输**向导在数据库之间复制数据或将数据提取到文件。

1. 右键单击表或模式。
2. 选择**数据 > 传输数据**。
3. 选择源（例如，一个表）和目标（另一个数据库连接或文件）。
4. 配置列映射和转换规则。
5. 执行传输。

### 执行计划 (EXPLAIN)

可视化查询执行计划，用于SQL调优。

1. 在SQL编辑器中编写查询。
2. 点击**解释计划**按钮（或右键单击 → **解释计划**）。
3. DBeaver 显示带有成本详情和索引使用情况的图形化计划。

### 比较工具 (Pro/Enterprise)

**结构比较**和**数据比较**工具允许您对两个数据库或环境之间的模式或数据进行差异比较。

- 在商业版中可用。

## 配置与自定义

### 连接设置

- **驱动属性**：从连接编辑器中修改JDBC驱动属性（例如超时、SSL模式、块大小）。
- **SSH隧道**：配置SSH隧道以安全访问远程数据库（在连接设置的**SSH**选项卡中）。
- **SSL**：通过**SSL**选项卡启用SSL并导入证书。

### 全局首选项

- `窗口 → 首选项` (Windows/Linux) 或 `DBeaver → 首选项` (macOS)。
- **外观**：在浅色/深色主题之间切换，调整字体大小。
- **编辑器**：配置SQL格式化样式、自动补全行为和执行选项。
- **连接**：设置默认事务隔离级别、自动提交和空闲超时。

### 驱动管理

- **驱动管理器**：`数据库 → 驱动管理器`。查看、编辑或添加自定义JDBC驱动。
- 首次连接到数据库时，直接从 DBeaver 的驱动仓库下载缺失的驱动。

## 自动化与脚本

### DBeaver CLI（仅限 Pro/Enterprise）

DBeaver Pro/Enterprise 包含一个命令行工具 (`dbeaver-cli`)，可在没有 GUI 的情况下执行 SQL 脚本、导出数据或运行任务。

```bash
# Connect and run a script against a PostgreSQL instance
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### 任务调度器 (Pro/Enterprise)

使用内置调度器（类 cron 界面）安排定期导出、数据传输或 SQL 脚本。

## 集成

- **版本控制**：Git 集成插件（社区版可用）– 提交 SQL 脚本或与已提交版本比较。
- **Docker**：使用 CLI 版本可以直接在容器中运行 DBeaver，用于 CI/CD 管道。
- **云数据库**：为 Snowflake、Amazon Redshift、Google BigQuery、Azure SQL 等预先配置的驱动。
- **SSH/SSL**：内置对安全连接和代理认证的支持。

## 兼容性与性能

| 方面 | 详情 |
|--------|---------|
| **支持的操作系统** | Windows 10+、macOS 10.15+、Linux (x64、amd64、aarch64) |
| **Java 要求** | JDK 11 或更高版本（安装程序自带） |
| **数据库支持** | 通过 JDBC/ODBC 支持 100+ 种数据库（包括关系型、类似 NoSQL、云数据库） |
| **性能提示** | - 对大型查询使用索引。<br>- 在首选项中关闭空闲连接。<br>- 对批量操作启用 **“使用批量更新”**。<br>- 对于非常大的数据集，分块导出或使用专用迁移工具。 |

## 故障排除与常见问题

### 常见问题

1. **“未找到驱动” / “无法连接”**
   - DBeaver 会提示下载驱动。如果自动下载失败，请转到 `数据库 → 驱动管理器`，选择您的数据库，然后点击**下载/更新**。
   - 确保可以访问互联网，或手动将 JAR 文件放入驱动库。

2. **连接挂起或超时**
   - 检查网络连通性和防火墙规则。
   - 检查 SSH/SSL 设置；配置错误的隧道可能会阻止连接。
   - 增加驱动属性中的连接超时。

3. **SQL 编辑器性能缓慢**
   - 禁用自动元数据加载：`首选项 → 数据库 → 导航器 → 禁用惰性元数据读取`。
   - 减少编辑器工具栏中的结果集限制。

4. **无法编辑 BLOB/CLOB**
   - DBeaver 支持小对象的内联编辑。对于大对象，使用**查看/编辑值**对话框（右键单击单元格 → **查看值**）。

### 常见问题解答

**问：DBeaver 完全免费吗？**
答：社区版是免费且开源的 (Apache 2.0)。Pro、Enterprise 和 Team 版是商业版，增加了 NoSQL 支持、AI 辅助和 CLI 等功能。

**问：我可以将 DBeaver 用于生产数据库吗？**
答：可以，社区版已准备好用于开发和 DBA 任务的生产环境。对于关键任务环境，请考虑具有额外支持和审计功能的 Enterprise 版。

**问：DBeaver 是否支持 MongoDB 或其他 NoSQL 数据库？**
答：社区版提供基本的 MongoDB 支持。完整的 NoSQL 和云数据库支持（包括 MongoDB、Cassandra 和 DynamoDB）在 Enterprise 版中可用。

**问：如何完全卸载 DBeaver？**
答：使用系统的包管理器（例如 `brew uninstall --cask dbeaver-community`、`snap remove dbeaver-ce`）或操作系统卸载程序。用户设置存储在 macOS/Linux 的 `~/.dbeaver` 或 Windows 的 `%APPDATA%\DBeaver` 中；删除这些目录以清除所有配置。

## 结论

DBeaver 是一款强大、灵活且用户友好的数据库工具，可无缝融入任何开发人员的工作流程。其开源核心、广泛的数据库支持和丰富的功能集使其成为任何处理数据的人的必备工具。

有关更多信息，请访问官方文档 [dbeaver.com/docs](https://dbeaver.com/docs/) 或在 [GitHub](https://github.com/dbeaver/dbeaver) 上为社区做出贡献。