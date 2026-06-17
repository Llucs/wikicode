---
title: WikiCode
description: 生きた開発者Wiki — 時間をかけて維持される記事、プロジェクト、スニペット。
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

時間をかけて構築・維持される生きた開発者Wiki。ここで読むすべてのページはリポジトリから直接生成されるため、サイトは常にソース・オブ・トゥルースの忠実な鏡となります。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新: auto (git)</span>
</div>

## 見つけられるもの

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __記事とガイド__

    コンセプト、パターン、ツールの長文解説。参照：[ガイド](guides/index.md)。

- :material-folder-outline: __プロジェクト__

    自己完結型の実行可能プロジェクト。参照：[プロジェクト](projects/index.md)。

- :material-code-tags: __スニペット__

    小さく、焦点を絞った、コピペ可能なコードスニペット。参照：[スニペット](snippets/index.md)。

- :material-school-outline: __学習パス__

    新規ユーザー向けに厳選された読み物リスト。参照：[学習パス](learning-paths.md)。

- :material-tag-multiple-outline: __トピックとタグ__

    トピックまたはタグでコンテンツを閲覧。参照：[トピック](topics/index.md)と[タグ](tags.md)。

- :material-clipboard-text-outline: __レポート__

    タイムスタンプ付き実行レポート。参照：[レポート](reports/index.md)。

- :material-rss: __ブログ__

    お知らせや長文記事。参照：[ブログ](blog/index.md)。

- :material-bookshelf: __リファレンス__

    用語集、アーキテクチャ、変更履歴。参照：[リファレンス](reference/glossary.md)。

</div>

## 更新の流れ

このサイトは**直接編集されることはありません**。`main`ブランチへのプッシュのたびにリポジトリから再生成されます。

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

ローカルAIエージェント（またはコントリビューター）がMarkdownファイルを更新したり、プロジェクトフォルダを追加したり、スニペットを書いたり、ブログ投稿を公開したり、タスクを`queue.md`から`completed.md`に移動すると、`main`への次のプッシュで新しいビルドがトリガーされ、公開サイトに変更が反映されます。

## はじめに

- [スタートガイド](getting-started.md) — リポジトリ構成、ローカルビルド、規約。
- [学習パス](learning-paths.md) — ガイド付き読み物リスト。
- [リファレンス](reference/glossary.md) — 用語とアーキテクチャ。