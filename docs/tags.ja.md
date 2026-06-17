---
title: タグ
description: WikiCodeで使用されるすべてのタグ。
created: 2026-06-03
tags:
  - meta
status: stable
---

# タグ

WikiCode全体で使用されるすべてのタグ。ページのfrontmatterから自動生成されます。タグをクリックすると、そのタグが付いているすべてのページが表示されます。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新日: auto (git)</span>
</div>

<div id="tag-list" markdown>
!!! info "自動タグ一覧"

    タグとそれに関連するページの一覧は、ビルド時に `docs/`、`projects/`、`snippets/` 内のすべてのMarkdownファイルのfrontmatterから生成されます。ページのメタデータ内のタグをクリックすると、Materialテーマがタグごとのページをレンダリングします。
</div>

## タグの追加

任意のページのfrontmatterにタグを追加します：

```yaml
---
title: My page
tags:
  - guide
  - backend
---
```

既存のタグを再利用することを推奨します。新しいタグが必要な場合は、[Guides](guides/index.md#suggested-tags)の推奨タグ一覧に追加して、他の作成者が見つけて再利用できるようにしてください。