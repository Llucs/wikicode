---
title: 标签
description: WikiCode 中使用的所有标签。
created: 2026-06-03
tags:
  - meta
status: stable
---

# 标签

所有在 WikiCode 中使用的标签，从页面前置数据自动生成。点击标签查看所有包含该标签的页面。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建于：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：自动（git）</span>
</div>

<div id="tag-list" markdown>
!!! info "自动标签列表"

    标签列表以及与之关联的页面是在构建时从 `docs/`、`projects/` 和 `snippets/` 中每个 Markdown 文件的前置数据生成的。Material 主题在您点击页面元数据中的任何标签时会呈现一个按标签分类的页面。
</div>

## 添加标签

在任何页面的前置数据中添加标签：

```yaml
---
title: My page
tags:
  - guide
  - backend
---
```

建议优先使用现有标签。如果需要新标签，请将其添加到[指南](guides/index.md#suggested-tags)的建议列表中，以便其他作者能够找到并复用。