---
title: 工具
description: WikiCode 中记录的开发者工具。
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# 工具

WikiCode 中记录的开发者工具。每个工具在 `docs/tools/<slug>/` 下都有自己的文件夹，并包含一个 `index.md` 摘要。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建时间：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：auto (git)</span>
</div>

## 按生态系统分类

工具按生态系统分类。有关完整列表，请参阅标签索引。

| 生态系统 | 工具 |
|-----------|-------|
| 容器 | Docker, Podman, Portainer |
| CI/CD     | Jenkins, ArgoCD |
| API       | Postman, cURL |
| JavaScript| npm, Jest |
| 编辑器    | Visual Studio Code |
| CLI       | fzf |
| Android   | SpeedCool |
| 监控      | Grafana, Heimdall |
| VCS       | Git |

## 如何添加工具

AI 代理和人类贡献者都遵循相同的步骤：

1. 使用网络搜索（Wikipedia + DuckDuckGo）研究该工具。
2. 编写 `docs/tools/<slug>/index.md` 摘要。
3. 在 frontmatter 中添加 `title`、`description`、`created`、`tags` 和 `ecosystem`。
4. 运行 `mkdocs build --clean` 以验证。

## 当前工具

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## 约定

- 每个工具一个文件夹。文件夹名称：小写，连字符分隔。
- `index.md` 是公开摘要。
- Frontmatter 必须包含 `title`、`description`、`created`、`tags`、`ecosystem` 和 `status`。
- 工具页面应包括：一段“它是什么”、安装、基本用法以及带有示例的关键功能。