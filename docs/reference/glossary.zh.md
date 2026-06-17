---
title: 术语表
description: 用于整个 WikiCode 的术语。
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# 术语表

WikiCode 使用的规范术语。定义简短，并链接到权威来源（如果有用）。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：auto (git)</span>
</div>

## 核心概念

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>仓库及其生成的静态网站。根据上下文，“WikiCode”可以指代两者之一。</dd>

<dt markdown>**文章**</dt>
<dd markdown>`docs/` 下的长篇 Markdown 页面。文章旨在完整阅读。</dd>

<dt markdown>**项目**</dt>
<dd markdown>`projects/` 下的自包含、可运行的软件单元。每个项目都有自己的 `README.md`、`index.md` 和源代码树。</dd>

<dt markdown>**代码片段**</dt>
<dd markdown>`snippets/` 下的小型、聚焦、可运行的代码单元。代码片段旨在复制和改编。</dd>

<dt markdown>**报告**</dt>
<dd markdown>`reports/` 下的一个带时间戳的 Markdown 文件，描述单次执行。格式：`YYYY-MM-DD-<slug>.md`。</dd>

<dt markdown>**决策**</dt>
<dd markdown>记录在 `memory/decisions.md` 中的架构或操作选择，带有四位数字和状态。</dd>

<dt markdown>**代理**</dt>
<dd markdown>任何遵循 `AGENT.md` 在仓库上工作的人类或自主过程。</dd>

<dt markdown>**任务**</dt>
<dd markdown>列在 `tasks/queue.md` 中的单个工作单元。每次执行一个任务。</dd>
</dl>

## 工作流术语

<dl markdown>
<dt markdown>**推送到 `main`**</dt>
<dd markdown>触发 `pages.yml`，重建并部署网站。对已发布网站的每个更改都通过此机制发生。</dd>

<dt markdown>**代理运行**</dt>
<dd markdown>由 `.github/workflows/wikicode-agent.yml` 触发的执行，可以通过 `workflow_dispatch`、问题上的 `@agent` 提及或标记为 `agent` 的问题触发。</dd>

<dt markdown>**前置数据**</dt>
<dd markdown>位于 Markdown 文件顶部、由 `---` 分隔的 YAML 元数据。WikiCode 至少需要 `title`、`description` 和 `created`。</dd>

<dt markdown>**标签**</dt>
<dd markdown>在前置数据中声明的标签，用于分组相关页面。Material 会自动生成按标签索引的页面。</dd>
</dl>

## 状态值

页面和项目可以在其前置数据中声明 `status`：

| 状态        | 含义                                                         |
| ----------- | --------------------------------------------------------------- |
| `draft`     | 进行中；可能不完整或错误。                                        |
| `stable`    | 已审阅并认为是正确的。可能仍会演变。                              |
| `archived`  | 保留以供参考；不再维护。                                         |
| `deprecated`| 已被其他内容取代；保留用于历史背景。                              |

`status: stable` 是所有已发布内容的默认期望。