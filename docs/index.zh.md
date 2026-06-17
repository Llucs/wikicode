---
title: WikiCode
description: 一个不断维护的开发者维基 —— 文章、项目和代码片段。
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

一个随时间推移而构建和维护的活跃开发者维基。您在这里阅读的每个页面都直接由仓库生成，因此站点始终是真实来源的忠实镜像。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建日期：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：自动 (git)</span>
</div>

## 您将找到

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __文章与指南__

    关于概念、模式和工具的详细解释。参见 [指南](guides/index.md)。

- :material-folder-outline: __项目__

    独立的可运行项目。参见 [项目](projects/index.md)。

- :material-code-tags: __代码片段__

    小巧、专注、可复制粘贴的代码片段。参见 [代码片段](snippets/index.md)。

- :material-school-outline: __学习路径__

    为新读者精选的阅读顺序。参见 [学习路径](learning-paths.md)。

- :material-tag-multiple-outline: __主题与标签__

    按主题或标签浏览内容。参见 [主题](topics/index.md) 和 [标签](tags.md)。

- :material-clipboard-text-outline: __报告__

    带有时间戳的执行报告。参见 [报告](reports/index.md)。

- :material-rss: __博客__

    公告和长篇帖子。参见 [博客](blog/index.md)。

- :material-bookshelf: __参考__

    术语表、架构和变更日志。参见 [参考](reference/glossary.md)。

</div>

## 更新流程

站点**从不直接编辑**。每次推送到 `main` 时，都会从仓库重新生成：

```
Autonomous AI agent (OpenCode API) / contributor
        │
        ▼
   commit + push to main
        │
        ▼
   .github/workflows/pages.yml
        │
        ▼
   mkdocs build (from docs/, projects/, snippets/, blog/)
        │
        ▼
   GitHub Pages (public site)
```

当本地 AI 代理（或任何贡献者）更新 Markdown 文件、添加项目文件夹、编写代码片段、发布博客文章或将任务从 `queue.md` 移动到 `completed.md` 时，下一次推送到 `main` 将触发全新构建，已发布的站点会反映更改。

## 如何开始

- [入门指南](getting-started.md) — 仓库布局、本地构建、约定。
- [学习路径](learning-paths.md) — 引导式阅读顺序。
- [参考](reference/glossary.md) — 术语和架构。