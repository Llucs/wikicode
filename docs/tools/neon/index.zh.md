---
title: Neon – Serverless PostgreSQL 平台
description: Neon 是一个开源 serverless PostgreSQL 数据库，它分离了计算与存储，为现代应用提供了即时分支、scale‑to‑zero 和 bottomless storage 功能。
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – Serverless PostgreSQL 平台

Neon 是一个开源、serverless PostgreSQL 平台，在云原生基础上重建了经典数据库架构。通过完全解耦计算（查询处理）和存储（数据持久化），Neon 提供了以前仅在 Amazon Aurora 等专有系统中才有的功能——但面向整个 Postgres 生态系统。借助即时分支、自动 scale‑to‑zero 和 bottomless storage，Neon 专为现代开发工作流和 serverless 应用程序设计。

---

## 为什么选择 Neon？

| 挑战 | Neon 解决方案 |
|-----------|---------------|
| **昂贵的空闲数据库** | 计算端点在不活动后缩放到 zero；您只需为活跃的计算付费。 |
| **缓慢的开发周期** | 即时分支为每个开发者/PR 提供其自己的全保真数据库分支。 |
| **存储配置与成本** | Bottomless storage 底层由对象存储（例如 S3）支持；无需手动容量规划。 |
| **Serverless/边缘兼容性** | 冷启动时间约 500 ms，结合 PgBouncer 池化为临时计算提供连接池。 |
| **向量工作负载** | 完全支持 `pgvector` 和 PostGIS；直接在 Postgres 中运行 AI 嵌入。 |

---

## 主要特性

### 1. Instant Branching

使用写时复制技术，Neon 可以在毫秒内创建一个 TB 级数据库的分支。这在以下场景中非常宝贵：

- **开发沙箱** – 每个开发者都可以获得生产环境的隔离克隆。
- **CI/CD 流水线** – 针对镜像生产数据的分支运行集成测试。
- **Schema 迁移** – 无风险地测试破坏性变更。

```bash
# 从主分支创建一个新分支
npx neonctl branches create --name feature/ai-search
```

### 2. Scale‑to‑Zero

计算端点在一段时间不活动后自动挂起。当新连接到达时，端点在约 500 ms 内恢复（cold start）。这消除了空闲或低流量数据库的成本。

```sql
-- 无需配置 – scale‑to‑zero 是自动的。
-- 连接后，端点将透明地唤醒。
```

### 3. Bottomless Storage

存储由单独的引擎（Pageserver + Safekeepers）处理，底层由廉价的对象存储支持。您永远不需要配置磁盘或担心存储空间不足。

### 4. Full PostgreSQL Compatibility

Neon 支持 PostgreSQL 14–17，包括所有主要扩展：

- `pgvector` – 用于嵌入的向量相似性搜索
- `PostGIS` – 地理空间查询
- `pg_cron`, `pg_stat_statements` 等

您现有的工具和驱动程序无需更改即可正常工作。

### 5. Transparent Connection Pooling

PgBouncer 集成在代理层面，因此无需任何应用程序配置即可获得高效的连接管理。

---

## 快速开始

### 选项 A：云（托管）

1. 在 [console.neon.tech](https://console.neon.tech) 注册（包含慷慨的免费套餐）。
2. 通过 UI 或 CLI 创建项目：

   ```bash
   # 安装 Neon CLI
   npx neonctl

   # 创建项目（首次：交互式）
   npx neonctl create-project

   # 获取主分支的连接字符串
   npx neonctl connection-string
   ```

### 选项 B：自托管

克隆开源仓库并使用 Docker Compose 或 Helm 部署。

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

生产部署请参考 [官方自托管指南](https://neon.tech/docs/self-host)。

---

## 使用示例

### 连接并运行查询

```bash
psql "postgresql://user:pass@ep-cool-123456.us-east-2.aws.neon.tech/neondb"
```

```sql
-- 标准 Postgres – 一切正常
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- pgvector 示例
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    embedding vector(1024)
);
```

### 创建和切换分支

```bash
# 列出分支
npx neonctl branches list

# 从特定时间点创建分支（时间旅行）
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# 使用分支：获取其连接字符串
npx neonctl connection-string --branch feature/ai-search
```

### 与 Vercel / Netlify 集成

因为 Neon 通过 `@neondatabase/serverless` 支持 HTTP 连接，您可以从边缘函数连接：

```javascript
// 示例：Next.js API 路由
import { neon } from '@neondatabase/serverless';

export default async function handler(req, res) {
  const sql = neon(process.env.DATABASE_URL);
  const result = await sql`SELECT * FROM events`;
  res.json(result);
}
```

---

## 架构简介

```
 应用程序
    |
    | (PostgreSQL 协议)
    |
 代理 ─── PgBouncer（连接池化）
    |
 计算节点（无状态 Postgres 进程）
    |
 Pageserver（存储引擎）
    |
 Safekeeper（WAL 持久化）
    |
 对象存储（S3、GCS 等）
```

- **计算节点** 是无状态的，可以水平扩展。
- **Pageserver** 负责页面服务、检查点和分支（写时复制）。
- **Safekeeper** 确保在确认之前 WAL 的持久化。

---

## 定价模式

Neon 是 **基于使用量** 计费的：

| 资源 | 免费套餐 | 付费套餐 |
|----------|-----------|-----------|
| 计算（活跃） | 10 小时/月 | 按计算小时付费 |
| 存储 | 500 MB | $0.12/GB/月 |
| 分支 | 无限制 | 无限制 |
| 连接池 | 是 | 是 |

Scale‑to‑zero 意味着您只需在应用程序实际处理查询时支付计算费用。

---

## 限制与注意事项

- **Cold start 延迟** – 虽然约 500 ms，但在延迟敏感的函数中可能较为明显。对于关键路径，建议使用长连接或 always‑on 端点。
- **功能对等性** – 仅支持单服务器部署（无原生分片）。对于多区域主动‑主动部署，可能仍需要外部复制策略。
- **免费套餐上限** – 如果多个项目保持活跃，10 计算小时的配额可能很快用完。

---

## 资源

- [官方文档](https://neon.tech/docs)
- [GitHub 仓库](https://github.com/neondatabase/neon)
- [Neon Discord 社区](https://discord.gg/neon)
- [博客 – 理解 Neon 架构](https://neon.tech/blog/architecture)

Neon 将 PostgreSQL 转变为真正的 serverless 数据库，使其成为现代应用程序、CI/CD 和 AI/向量工作负载的理想选择。它结合了即时分支、scale‑to‑zero 和完全 Postgres 兼容性，使其成为 2024–2026 年最受欢迎的基础设施项目之一。