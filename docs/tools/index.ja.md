---
title: ツール
description: WikiCodeで文書化された開発ツール。
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# ツール

WikiCodeで文書化されている開発ツール。
各ツールには `docs/tools/<slug>/` の下に独自のフォルダがあり、`index.md` のサマリーが含まれています。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新: auto (git)</span>
</div>

## エコシステム別

ツールはエコシステム別に分類されています。完全なリストは tag index を参照してください。

| Ecosystem | Tools |
|-----------|-------|
| Container | Docker, Podman, Portainer |
| CI/CD     | Jenkins, ArgoCD |
| API       | Postman, cURL |
| JavaScript| npm, Jest |
| Editor    | Visual Studio Code |
| CLI       | fzf |
| Android   | SpeedCool |
| Monitoring| Grafana, Heimdall |
| VCS       | Git |

## ツールの追加方法

AIエージェントと人間の貢献者は同じ手順に従います。

1. ウェブ検索 (Wikipedia + DuckDuckGo) を使用してツールを調査します。
2. `docs/tools/<slug>/index.md` のサマリーを作成します。
3. `title`、`description`、`created`、`tags`、`ecosystem` を含む frontmatter を追加します。
4. `mkdocs build --clean` を実行して検証します。

## 現在のツール

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## 規約

- ツールごとに1つのフォルダ。フォルダ名: 小文字、ハイフン区切り。
- `index.md` は公開サマリーです。
- Frontmatter には `title`、`description`、`created`、`tags`、`ecosystem`、`status` を含める必要があります。
- ツールページには以下を含める必要があります: 1段落の「概要」、インストール、基本的な使い方、および例を含む主要機能。