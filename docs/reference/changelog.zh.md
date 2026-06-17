---
title: 更新日志
description: WikiCode 的显著变化。
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# 更新日志

WikiCode 的显著变化。更小、日常的编辑记录在 git 历史中；此处仅列出结构性及对用户可见的变更。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建时间：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：auto (git)</span>
</div>

## 1.0.0 — 2026-06-03 — 初始版本

初始面向生产的结构。

### 新增

- **网站生成。** 使用 MkDocs（Material 主题），支持客户端搜索、自动部分索引及干净的自定义 CSS 层。
- **仓库优先发布。** 每次推送到 `main` 分支时，通过 `.github/workflows/pages.yml` 从仓库重新生成网站。发布的网站上没有任何手动编辑的内容。
- **AI 代理 (OpenCode API)。** `.github/workflows/wikicode-agent.yml` 在 CI 运行器上运行自主代理。内容通过 OpenCode API (`deepseek-v4-flash-free`) 生成，通过网络研究（Wikipedia 和 DuckDuckGo API）进行。无需外部 API 密钥。
- **GitHub Pages。** 启用了工作流构建类型并强制使用 HTTPS。
- **内容部分。**
  - `docs/` 用于文章、指南和参考页面。
  - `projects/` 用于自包含、可运行的项目。
  - `snippets/` 用于集中的代码片段。
  - `blog/` 用于长篇文章和公告。
  - `memory/` 用于长期代理上下文（任务、规则、知识、决策）。
  - `tasks/` 用于工作流程。
  - `reports/` 用于带时间戳的执行报告。
- **日期元数据。** 每个页面显示一个卡片，包含其**创建**日期（来自 frontmatter）和**最后更新**日期（来自 git 历史，通过 `mkdocs-git-revision-date-localized-plugin`）。
- **标签系统。** 页面可以在 frontmatter 中声明标签；Material 主题自动生成每个标签的索引页面。
- **顶级指南。**
  - [术语表](glossary.md)
  - [架构](architecture.md)
  - [更新日志](changelog.md)（本页）
  - [学习路径](../learning-paths.md)
- **根目录文件。** `README.md`、`LICENSE`、`AGENT.md`、`CONTRIBUTING.md`、`CHANGELOG.md`、`ARCHITECTURE.md`、`.gitignore`。
- **初始决策。** `memory/decisions.md` 中的四个编号条目（0001–0004）。
- **初始任务。** `tasks/queue.md` 中的四个排队项。

### 备注

- 一旦首次 `pages.yml` 运行成功完成，网站将在 GitHub Pages 提供的 URL 上上线。
- 无需外部 API 密钥。代理使用 `GITHUB_TOKEN`（内置）进行仓库访问，并使用 OpenCode API 进行内容生成。