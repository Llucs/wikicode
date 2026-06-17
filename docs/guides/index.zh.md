---
title: 指南
description: 长篇、面向主题的指南。
created: 2026-06-03
tags:
  - meta
status: stable
---

# 指南

长篇指南按主题分组。每个指南是 `docs/guides/` 目录下（或子文件夹中）的一个实际 Markdown 文件。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建于：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：auto (git)</span>
</div>

## 约定

- 每个指南一个文件夹或 `.md` 文件。
- 文件夹名称：小写，连字符连接。
- Frontmatter 应包含 `title`、`description`、`created` 和 `tags`。
- 标签有助于交叉引用：尽量复用 [Tags](../tags.md) 中的现有标签，而不是发明新标签。

## 建议的标签

| 标签             | 含义                                                  |
| --------------- | -------------------------------------------------------- |
| `meta`          | 关于 WikiCode 本身的页面。                             |
| `guide`         | 如何使用的内容。                              |
| `reference`     | 参考资料（术语表、列表）。                  |
| `architecture`  | 维基如何构建和工作。                  |
| `process`       | 工作流程、贡献、治理。                     |
| `language-go`   | 主要内容涉及 Go。                              |
| `language-py`   | 主要内容涉及 Python。                          |
| `language-cpp`  | 主要内容涉及 C++。                             |
| `language-rs`   | 主要内容涉及 Rust。                            |
| `language-js`   | 主要内容涉及 JavaScript / TypeScript。        |
| `backend`       | 后端工程主题。                             |
| `frontend`      | 前端工程主题。                            |
| `devops`        | 构建、部署、可观察性。                            |
| `security`      | 安全主题。                                         |
| `data`          | 数据库、管道、分析。                         |

像这样将标签添加到 frontmatter：

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```