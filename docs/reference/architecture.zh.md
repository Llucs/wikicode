---
title: 架构
description: WikiCode 的构建方式以及如何保持更新。
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# 架构

WikiCode 的构建方式、保持最新的机制，以及自主代理如何融入工作流程。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建时间：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：自动 (git)</span>
</div>

## 高层架构图

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               │                  └──────────┬───────────┘
               │                             │
               ▼                             │
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` 代理使用 Wikipedia 和 DuckDuckGo API 进行网络研究，无需 API 密钥。

## 层次结构

### 1. 内容

纯 Markdown。编写无需特殊工具。

| 路径                | 用途                                                              |
| ------------------- | ----------------------------------------------------------------- |
| `docs/`             | 文章、指南、参考，你在网站上阅读的内容。                          |
| `docs/concepts/`    | 架构模式、设计原则、技术概念。                                    |
| `docs/guides/`      | 长篇、面向主题的指南。                                            |
| `docs/tools/`       | 每个记录的开发者工具对应一个文件夹。                              |
| `docs/analyses/`    | 平台/库的技术分析和架构研究。                                     |
| `docs/reference/`   | 词汇表、架构、变更日志。                                          |
| `docs/topics/`      | 主题索引。                                                        |
| `projects/`         | 真实、可运行的项目。每个都是一个独立的单元。                      |
| `snippets/`         | 小巧、聚焦、可运行的代码片段。                                    |
| `blog/`             | 较长的文章、公告、事后分析。                                      |
| `memory/`           | 代理的长期上下文（使命、规则、决策）。                            |
| `tasks/`            | 工作流水线（队列 + 已完成）。                                     |
| `reports/`          | 带时间戳的执行报告，按年/月组织。                                 |

### 2. 生成

- **MkDocs** 与 **Material** 主题将 Markdown 树转换为静态站点。
- 插件：
  - `search` — 客户端全文搜索。
  - `awesome-pages` — 自动生成章节索引。
  - `git-revision-date-localized` — 从 git 获取最后更新日期。
  - `blog` — Material 内置的博客支持。
  - `git-committers` — 可选，由环境变量控制。

### 3. 部署

- `pages.yml` 每次推送到 `main` 时运行。它构建站点并使用官方的 Pages actions（`actions/upload-pages-artifact` + `actions/deploy-pages`）部署到 **GitHub Pages**。
- Pages 配置为 `build_type: workflow` 并强制使用 HTTPS。

### 4. 自动化

#### 每日增长

`wikicode-agent.yml` 按**每日两次**的计划运行（`0 6,18 * * *`，UTC 时间 06:00 和 18:00），并支持手动触发。每次运行都是一个单一的、范围明确的更改，因此 wiki 每天都会增长一点。

每次运行的预期循环：

1. 工作流启动。安装 Python 依赖。
2. `scripts/agent.py` 读取 `memory/` 获取上下文。如果任务队列为空，它会主动发现需要记录的新工具和项目。然后通过 Wikipedia + DuckDuckGo API 研究选定的主题。
3. OpenCode API 生成内容（带 frontmatter 的 Markdown）。
4. 代理写入文件，运行 `mkdocs build --clean` 进行验证，然后提交并推送。
5. `pages.yml` 重新构建并部署站点。
6. 下一次运行时看到的 wiki 比之前稍大，然后继续。

#### 触发器

| 触发器                     | 用途                                                  |
| -------------------------- | ----------------------------------------------------- |
| `schedule`                 | 默认的增长运行（UTC 时间 06:00 和 18:00）。          |
| `workflow_dispatch`        | 从 Actions 标签页手动运行。                          |
| `issue_comment`            | 在 issue 或 PR 评论中提及 `@agent`。                 |
| `issues` with label        | 标记为 `agent` 的 issue。                            |

#### 并发

`concurrency: wikicode-agent` 设置为 `cancel-in-progress: true`，以便重叠的运行不会重复写入仓库。

### 5. 去重

WikiCode 不希望重复记录同一事物。去重机制包含三个部分：

1. **章节索引页面。** 每个章节都有一个 `index.md` 列出其当前内容。`awesome-pages` 插件会自动从文件系统发现列表，因此始终准确。
2. **`git grep` 回退。** 代理脚本扫描章节索引和任务列表，然后使用 `git grep` 确认主题是新的，然后再生成内容。
3. **知识账本。** `memory/knowledge.md` 列出了主要内容以及添加新内容的规则。

如果检测到重复，代理必须改进现有页面，而不是编写新页面（`memory/rules.md` 中的规则 16）。

### 6. 网络研究

代理使用 Wikipedia 和 DuckDuckGo API 收集需要记录的任何主题的信息。这是保持生成内容真实且最新的机制：

1. `scripts/agent.py` 中的 `research_topic()` 会为该主题运行 Wikipedia 搜索和 DuckDuckGo Instant Answer 查询。
2. Wikipedia 返回文章标题 + 介绍性摘录（纯文本，最多 2000 个字符）。
3. DuckDuckGo 返回摘要和相关主题。
4. 如果两者都返回空，代理将回退到 LLM 的训练知识。
5. 收集的研究文本被注入内容生成提示中，以便 LLM 根据真实世界的信息进行写作。

## 内容分类 v2

WikiCode 中的每个文档严格属于以下类别之一：

| 类别       | 路径                     | 内容                                              |
| ---------- | ------------------------ | ------------------------------------------------- |
| **概念**   | `docs/concepts/<slug>/`  | 架构模式、设计原则或技术概念。                    |
| **工具**   | `docs/tools/<slug>/`     | 开发者工具文档（安装、使用、功能）。              |
| **分析**   | `docs/analyses/<slug>/`  | 平台、框架或库的架构研究。                        |
| **项目**   | `projects/<slug>/`       | 真实、可运行的开源项目，附带设置指南。            |
| **指南**   | `docs/guides/`           | 长篇、面向主题的教程或操作指南。                  |
| **报告**   | `reports/YYYY/MM/`       | 带时间戳的执行记录，提交后不可更改。              |
| **记忆**   | `memory/`                | 代理上下文：使命、规则、决策、知识、状态、质量。  |

这种分离是语义上的，而非表面上的：

- **概念与指南** — 概念页面解释模式、原则或技术（例如微服务、CQRS、OAuth）。指南是叙述性的演练，可能跨越多个概念或工具。
- **工具与分析** — 工具页面教授*如何使用*某物（安装 → 配置 → 运行）。分析则研究*架构和权衡*（比较替代方案、评估设计决策）。
- **指南与工具** — 指南是跨越多个工具或概念的叙述性演练。工具页面是单一参考卡片。
- **报告作为记录** — 报告在提交后不可更改。它们按 `YYYY/MM/` 组织以防止扁平目录膨胀，并支持按时间顺序浏览。
- **记忆作为代理契约** — `memory/` 中的每个文件都有不同的角色（在 `memory/knowledge.md` 中声明）。代理在启动时读取所有文件；每次运行后也会写入 `state.md`。

## Frontmatter 契约

站点上的每个页面都应包含：

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title` 和 `description` 用于导航和搜索。`created` 提供元数据卡片；`git-revision-date-localized` 自动填充“最后更新”日期。`tags` 支持基于标签的浏览。`status` 表示页面的成熟度。

## 秘密与安全

| 秘密                 | 用途                              | 来源       |
| -------------------- | --------------------------------- | ---------- |
| `GITHUB_TOKEN`       | 工作流中的仓库访问。              | 内置。     |

仓库中不存储任何凭据。

## 如何演进架构

任何影响站点构建、部署或自动化的更改都应：

1. 作为新条目记录在 `memory/decisions.md` 中，使用下一个可用编号。
2. 如果改变高层架构图，应在本页面中体现。
3. 保持仓库优先原则：绝不直接编辑已发布的站点。