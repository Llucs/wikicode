---
title: 変更履歴
description: WikiCodeにおける注目すべき変更点。
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# 変更履歴

WikiCodeにおける注目すべき変更点。日々の細かい編集はgit履歴に記録されており、ここには構造的な変更やユーザーから見える変更のみを記載します。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新: 自動（git）</span>
</div>

## 1.0.0 — 2026-06-03 — Bootstrap

初期の本番向け構成。

### 追加

- **サイト生成。** MkDocs（Materialテーマ）を使用し、クライアントサイド検索、自動セクションインデックス、およびクリーンなカスタムCSSレイヤーを備える。
- **リポジトリ優先の公開。** `.github/workflows/pages.yml` を使用して、`main` ブランチにプッシュされるたびにリポジトリからサイトが再生成されます。公開サイトには手動で編集されたものはありません。
- **AIエージェント（OpenCode API）。** `.github/workflows/wikicode-agent.yml` はCIランナー上で自律エージェントを実行します。OpenCode API（`deepseek-v4-flash-free`）によるコンテンツ生成、WikipediaおよびDuckDuckGo APIによるWeb調査。外部APIキーは必要ありません。
- **GitHub Pages。** ワークフローのビルドタイプで有効化され、HTTPSが強制されます。
- **コンテンツセクション。**

  - `docs/` : 記事、ガイド、およびリファレンスページ用。
  - `projects/` : 自己完結型で実行可能なプロジェクト用。
  - `snippets/` : 焦点を絞ったコードスニペット用。
  - `blog/` : 長めの記事や告知用。
  - `memory/` : 長期的なエージェントコンテキスト用（ミッション、ルール、知識、決定事項）。
  - `tasks/` : 作業パイプライン用。
  - `reports/` : タイムスタンプ付き実行レポート用。

- **日付メタデータ。** 各ページには、**作成日**（フロントマターから）と**最終更新日**（git履歴から、`mkdocs-git-revision-date-localized-plugin` 経由）を示すカードが表示されます。
- **タグシステム。** ページはフロントマターでタグを宣言でき、Materialテーマが自動的にタグごとのインデックスページを生成します。
- **トップレベルガイド。**
  - [用語集](glossary.md)
  - [アーキテクチャ](architecture.md)
  - [変更履歴](changelog.md)（このページ）
  - [学習パス](../learning-paths.md)
- **ルートファイル。** `README.md`、`LICENSE`、`AGENT.md`、`CONTRIBUTING.md`、`CHANGELOG.md`、`ARCHITECTURE.md`、`.gitignore`。
- **初期の決定事項。** `memory/decisions.md` に4つの番号付きエントリ（0001–0004）。
- **初期タスク。** `tasks/queue.md` に4つのキューイングされたアイテム。

### 注記

- 最初の `pages.yml` の実行が正常に完了すると、サイトはGitHub Pagesが提供するURLで公開されます。
- 外部APIキーは不要です。エージェントはリポジトリアクセスに `GITHUB_TOKEN`（組み込み）を使用し、コンテンツ生成にOpenCode APIを使用します。