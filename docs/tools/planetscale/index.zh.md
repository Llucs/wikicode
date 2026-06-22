---
title: PlanetScale：无服务器MySQL数据库平台
description: 这是一个基于Vitess构建的完全托管的MySQL兼容数据库平台，它引入了数据库分支和无阻塞模式变更，适用于现代开发工作流。
created: 2026-06-22
tags:
  - database
  - mysql
  - vitess
  - serverless
  - schema-migration
  - devops
  - dbaas
  - branching
status: draft
---

# PlanetScale

## 简介

PlanetScale 由 Vitess 的核心创建者（Sugu Sougoumarane、Jiten Vaidya 和 Morgan Goeller）于 2018 年创立，是一个基于为 YouTube 提供支持的开源数据库集群系统构建的 MySQL 兼容数据库平台。它通过将 **Git 风格的工作流**——数据库分支和 Deploy Requests——应用于模式和数据，重新定义了数据库管理。

这种方法消除了传统模式迁移带来的瓶颈和停机时间，使数据库变更变得像代码变更一样安全、可审查和可迭代。PlanetScale 是一项完全托管服务，负责处理复制、备份、分片和高可用性，同时支持无服务器计算层，该层可伸缩至零并在连接时立即唤醒。

## 核心概念

### 数据库分支
正如 `git branch` 允许隔离代码开发一样，`pscale branch create` 会在 PlanetScale 的基础设施上创建一个隔离的、功能完整的数据库副本（包括数据和模式）。

- **从任意点分支：** 从 `main` 或之前的快照创建分支。
- **数据与模式：** 分支包含完整的快照，从而实现高度真实的测试。
- **临时性：** 分支旨在完成其使命后被丢弃，防止模式漂移。

### Deploy Requests（DRs）
PlanetScale 对应 Pull Request 的机制。当您对分支上的模式更改感到满意时，您可以开启一个 Deploy Request。这将生成差异，支持审查，并将合并作为**无阻塞在线模式迁移**（使用 Vitess VReplication）执行。

### 无服务器计算
PlanetScale 将计算与存储分离。数据库在没有活动连接时处于“休眠”状态。连接会立即唤醒数据库，从而消除空闲计算成本。

## 入门指南

### 安装
主要的开发者接口是 `pscale` CLI。

**macOS:**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows:**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### 身份验证
```bash
pscale auth login
```

### 创建数据库
```bash
pscale database create my-app
```

### 使用分支

**创建一个功能分支（从 main 复制模式和数据）：**
```bash
pscale branch create my-app feature-user-profile
```

**连接到分支：**
```bash
pscale connect my-app feature-user-profile --port 3309
```
这会运行一个本地代理。您的应用程序连接到 `127.0.0.1:3309`。该代理会自动处理身份验证。

**在分支上运行模式迁移：**
使用任何 MySQL 客户端、ORM 或迁移工具（例如 `mysql2`、`Prisma`、`SQLAlchemy`）。
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### Deploy Request 流程
在您对分支上的模式更改进行了全面测试之后：

```bash
# 创建 Deploy Request
pscale deploy-request create my-app feature-user-profile

# 列出 deploy requests
pscale deploy-request list my-app

# 部署请求（审查后）
pscale deploy-request deploy my-app <deploy-number>

# 清理分支
pscale branch delete my-app feature-user-profile --force
```

部署操作会将模式更改应用到 `main`，*而不会锁定表或造成停机*。

## 关键特性详解

### 无阻塞模式更改（在线 DDL）
MySQL 中传统的 `ALTER TABLE` 语句通常会锁定表。PlanetScale 通过 VReplication 使用 Vitess 的**在线 DDL**。它会创建一个影子表，逐步复制数据，并透明地进行切换。

**命令示例：**
```bash
pscale deploy-request deploy my-app 1
```
即使在大型、长时间运行的迁移过程中，生产环境也能完全正常运行。

### 连接池
内置的服务器端连接池可管理连接峰值。使用 `pscale connect` 时，本地代理也会池化连接。对于生产环境，请直接连接到 PlanetScale 服务器地址。

### 水平分片（Vitess）
对于超大数据集，PlanetScale 使用 Vitess 的键范围分片将数据透明地分布到多个 MySQL 实例中。无需更改应用程序。

### 高可用性与全局复制
高可用性是内建的。PlanetScale 提供跨区域副本和自动故障转移，SLA 高达 99.99%。

## 实际用例

### CI/CD 集成
为每个 Pull Request 启动一个隔离的数据库分支，以针对真实生产数据运行集成测试。
```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# 在此处运行集成测试
pscale branch delete my-app ci-pr-123 --force
```

### 预生产测试
让 QA 在完全真实的分支上运行破坏性测试或负载测试，而不会破坏生产数据。

### 模式审查
团队成员可以在合并前在 Deploy Request 中审查确切的 SQL 差异，从而实现“数据库即代码”的工作流。

### 临时环境
将 `pscale branch create/destroy` 与平台工程工具（例如 Kubernetes operators、Terraform）结合使用，为每个开发者或每个功能提供全栈环境。

## 限制与注意事项

虽然功能强大，但 PlanetScale 基于 Vitess 的特性引入了一些 MySQL 兼容性问题：

- **不支持存储过程和触发器：** Vitess 代理层不支持这些。
- **外键：** 处于测试阶段（必须按数据库启用）。目前不建议用于关键生产路径。
- **`LOCK TABLES` / `UNLOCK TABLES`：** 不支持。
- **`GET_LOCK()` / `RELEASE_LOCK()`：** 不支持。
- **子查询与 `JOIN`：** 大多数受支持，但非常复杂的相关子查询或非确定性语句可能表现不同。
- **直接对生产环境执行 `ALTER TABLE`：** Deploy Request 工作流是对生产环境进行模式更改的*唯一*安全方式。强烈建议不要通过 `pscale connect` 在生产分支上直接运行 `ALTER TABLE`。

> **开发者须知：** 对**生产**环境的模式更改始终使用 Deploy Request 工作流。对于开发分支，直接使用 `ALTER TABLE` 是安全且快速的。

## 定价模式

PlanetScale 以 SaaS 产品形式运营，提供慷慨的免费套餐。定价基于行存储和行读写量。

| 套餐 | 价格 | 行存储 | 计算 | 分支数量 |
|---|---|---|---|---|
| **免费** | $0/月 | 5 GB | 每月 1000 万次行读取，100 万次行写入 | 最多 3 个 |
| **Scaler** | $39/月（基础） | 10 GB | 每月 1 亿次行读取，1000 万次行写入 | 最多 10 个 |
| **Business** | 自定义 | 自定义 | 自定义 | 自定义 |

*定价细节可能变化；请始终在 [PlanetScale 定价页面](https://planetscale.com/pricing) 上进行验证。*

## 最佳实践

- **分支命名：** 使用一致的命名空间（例如 `feature/*`、`hotfix/*`、`ci/*`）。
- **销毁过期分支：** 定期清理分支以避免存储成本。
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **监控性能：** 使用 PlanetScale 仪表盘监控查询性能、慢查询和连接使用情况。查询解释和洞察功能非常强大。
- **环境一致性：** 保持 `main` 为纯净的生产环境。开发团队仅在分支上工作。
- **避免在生产分支代理上运行重型查询：** 虽然分支是一个快照，但在与生产环境相同的底层集群上连接的分支上运行大量分析查询可能会影响共享 I/O。

## 故障排除

**代理连接被拒绝：**
```bash
pscale connect my-app main
```
确保没有其他服务正在使用该端口。使用 `--port` 指定其他端口。

**模式更改失败：**
在 PlanetScale 仪表盘中检查 Deploy Request 日志，或使用：
```bash
pscale deploy-request show my-app <deploy-number>
```

**查询延迟高：**
验证连接池限制。考虑在合并前向分支添加索引：
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## 替代方案对比

| 特性 | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **分支功能** | 即时，包含完整数据 | 即时，包含完整数据 | 通过 SQL 分支 | 手动快照 |
| **无服务器** | 是（休眠/唤醒） | 是（休眠/唤醒） | 是（自动挂起） | 否（始终开启） |
| **模式迁移** | 无阻塞（在线 DDL） | 分支 + `pgroll` | 分支 + 迁移 | 手动 |
| **分片** | 自动（Vitess） | 否 | 否 | 手动（分片） |
| **迁移 CI 流程** | 优秀（Deploy Requests） | 优秀 | 良好 | 差 |

**何时选择 PlanetScale：**
您需要 MySQL 兼容性、用于复杂模式更改和测试的数据库分支，以及自动水平扩展。

**何时避免使用 PlanetScale：**
您严重依赖存储过程、触发器或高级 MySQL 内部特性（例如 `GET_LOCK()`）。在这种情况下，RDS 或标准的托管 MySQL 解决方案可能更适合。

## 总结

PlanetScale 通过将类似 Git 的工作流引入数据库层，彻底改变了 MySQL 的开发体验。其即时分支数据和模式的能力，结合无阻塞的 Deploy Requests，使得团队能够以与应用代码相同的安全性和速度迭代数据库模式。基于久经考验的 Vitess 引擎构建，它提供了 YouTube 级别的可扩展性，而无需运营开销。