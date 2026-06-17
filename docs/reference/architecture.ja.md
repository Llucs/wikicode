---
title: アーキテクチャ
description: WikiCodeはどのように構築され、最新の状態に保たれているか。
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# アーキテクチャ

WikiCodeの構築方法、最新状態の維持方法、そして自律エージェントがどのようにループに組み込まれているかについて。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新日: auto (git)</span>
</div>

## ハイレベル図

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               │                  └──────────┬───────────┘
               │                             │
               ▼                             │
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` The agent uses Wikipedia and DuckDuckGo APIs for web research,
no API keys required.

## レイヤー

### 1. コンテンツ

プレーンなMarkdownです。作成に特別なツールは必要ありません。

| Path               | Purpose                                                                 |
| ------------------ | ----------------------------------------------------------------------- |
| `docs/`            | 記事、ガイド、リファレンス、サイトで読むもの。                              |
| `docs/concepts/`   | アーキテクチャパターン、設計原則、技術的概念。                              |
| `docs/guides/`     | 長く、トピック指向のガイド。                                               |
| `docs/tools/`      | 文書化された開発者ツールごとに1フォルダ。                                   |
| `docs/analyses/`   | プラットフォームやライブラリの技術分析とアーキテクチャ研究。                    |
| `docs/reference/`  | 用語集、アーキテクチャ、変更ログ。                                          |
| `docs/topics/`     | トピックインデックス。                                                    |
| `projects/`        | 実際に実行可能なプロジェクト。それぞれが自己完結したユニットです。              |
| `snippets/`        | 小さく、焦点を絞った、実行可能なコードスニペット。                           |
| `blog/`            | より長い記事、発表、事後分析。                                              |
| `memory/`          | エージェントのための長期的なコンテキスト（ミッション、ルール、決定事項）。      |
| `tasks/`           | 作業パイプライン（キュー＋完了済み）。                                      |
| `reports/`         | タイムスタンプ付きの実行レポート。年/月で整理。                              |

### 2. 生成

- **MkDocs**と**Material**テーマを使用して、Markdownツリーを静的サイトに変換します。
- プラグイン：
  - `search` — クライアントサイドの全文検索。
  - `awesome-pages` — 自動セクションインデックス。
  - `git-revision-date-localized` — gitから最終更新日を取得。
  - `blog` — Materialの組み込みブログサポート。
  - `git-committers` — オプション。環境変数で制御。

### 3. デプロイ

- `pages.yml`は`main`へのプッシュごとに実行されます。公式のPagesアクション（`actions/upload-pages-artifact` + `actions/deploy-pages`）を使用してサイトをビルドし、**GitHub Pages**にデプロイします。
- Pagesは`build_type: workflow`で構成され、HTTPSが強制されます。

### 4. 自動化

#### 日次の成長

`wikicode-agent.yml`は**1日2回のスケジュール**（`0 6,18 * * *`、06:00および18:00 UTC）と手動トリガーで実行されます。各実行は単一のスコープ化された変更であり、Wikiは毎日少しずつ成長します。

実行ごとの期待されるループ：

1. ワークフローが開始されます。Pythonの依存関係がインストールされます。
2. `scripts/agent.py`がコンテキストのために`memory/`を読み取ります。タスクキューが空の場合、積極的に文書化する新しいツールやプロジェクトを発見します。その後、Wikipedia + DuckDuckGo APIを介して選択したトピックを調査します。
3. OpenCode APIがコンテンツ（フロントマター付きMarkdown）を生成します。
4. エージェントはファイルを書き込み、`mkdocs build --clean`を実行して検証し、コミットしてプッシュします。
5. `pages.yml`がサイトを再ビルドしてデプロイします。
6. 次の実行では、わずかに大きくなったWikiを参照して続行します。

#### トリガー

| Trigger                  | Use case                                                |
| ------------------------ | ------------------------------------------------------- |
| schedule                 | デフォルトの成長実行（06:00と18:00 UTC）。               |
| workflow_dispatch        | Actionsタブからの手動実行。                              |
| issue_comment             | IssueまたはPRコメントでの`@agent`メンション。             |
| issues with label        | `agent`ラベルが付いたIssue。                             |

#### 並行実行

`concurrency: wikicode-agent`が`cancel-in-progress: true`で設定されており、重複する実行がリポジトリに二重書き込みをしないようにしています。

### 5. 重複防止

WikiCodeは同じことを二度文書化することを望みません。重複排除メカニズムには3つの部分があります。

1. **セクションインデックスページ。** すべてのセクションには、現在のコンテンツを一覧表示する`index.md`があります。`awesome-pages`プラグインがファイルシステムからリストを自動検出するため、常に正確です。
2. **`git grep`フォールバック。** エージェントスクリプトはセクションインデックスとタスクリストをスキャンし、`git grep`を使用してトピックが新しいことを確認してからコンテンツを生成します。
3. **知識台帳。** `memory/knowledge.md`には、主要なコンテンツと新しいコンテンツを追加するためのルールがリストされています。

重複が検出された場合、エージェントは新しいページを作成する代わりに既存のページを改善する必要があります（`memory/rules.md`のルール16）。

### 6. Web調査

エージェントは、文書化が必要なあらゆるトピックに関する情報を収集するために、WikipediaおよびDuckDuckGoのAPIを使用します。これにより、生成されたコンテンツは事実に基づき最新の状態に保たれます。

1. `scripts/agent.py`の`research_topic()`は、トピックに対してWikipedia検索とDuckDuckGo Instant Answerクエリの両方を実行します。
2. Wikipediaは記事タイトルと導入部の抜粋（プレーンテキスト、最大2000文字）を返します。
3. DuckDuckGoは要約と関連トピックを返します。
4. 両方が空を返した場合、エージェントはLLMのトレーニング知識にフォールバックします。
5. 収集された調査テキストはコンテンツ生成プロンプトに注入され、LLMが実際の情報に基づいて記述するようにします。

## コンテンツ分類 v2

WikiCodeのすべてのドキュメントは、以下のカテゴリのいずれかに正確に属します。

| Category | Path                 | What goes there                                                      |
| -------- | -------------------- | -------------------------------------------------------------------- |
| 概念     | `docs/concepts/<slug>/` | アーキテクチャパターン、設計原則、または技術的概念。                     |
| ツール   | `docs/tools/<slug>/`   | 開発者ツールのドキュメント（インストール、使用方法、機能）。               |
| 分析     | `docs/analyses/<slug>/` | プラットフォーム、フレームワーク、またはライブラリのアーキテクチャ研究。    |
| プロジェクト | `projects/<slug>/`    | 実際に実行可能なオープンソースプロジェクト（セットアップガイド付き）。       |
| ガイド   | `docs/guides/`        | 長く、トピック指向のチュートリアルまたはハウツー。                         |
| レポート | `reports/YYYY/MM/`     | タイムスタンプ付き実行記録、コミット後は不変。                           |
| 記憶     | `memory/`             | エージェントコンテキスト：ミッション、ルール、決定事項、知識、状態、品質。  |

区別は意味論的なものであり、見た目の問題ではありません。

- **概念 vs ガイド** — 概念ページはパターン、原則、または技術（例：マイクロサービス、CQRS、OAuth）を説明します。ガイドは複数の概念やツールにわたるナラティブなウォークスルーです。
- **ツール vs 分析** — ツールページは何かの*使用方法*（インストール→設定→実行）を教えます。分析は*アーキテクチャとトレードオフ*を研究します（代替案の比較、設計判断の評価）。
- **ガイド vs ツール** — ガイドは複数のツールや概念にわたるナラティブなウォークスルーです。ツールページは単一のリファレンスカードです。
- **記録としてのレポート** — レポートはコミット後は不変です。フラットディレクトリの肥大化を防ぎ、時系列での閲覧を可能にするために`YYYY/MM/`で整理されています。
- **エージェント契約としての記憶** — `memory/`内のすべてのファイルには明確な役割があります（`memory/knowledge.md`で宣言）。エージェントは起動時にそれらすべてを読み取ります。各実行後には`state.md`も書き込まれます。

## フロントマター契約

サイト上のすべてのページには以下が必要です：

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title`と`description`はナビゲーションと検索で使用されます。`created`はメタデータカードに供給され、`git-revision-date-localized`が「最終更新日」を自動的に埋めます。`tags`はタグベースのブラウジングを可能にします。`status`はページの成熟度を示します。

## シークレットとセキュリティ

| Secret              | Purpose                                            | Source                |
| ------------------- | -------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`      | ワークフロー内でのリポジトリアクセス。                | 内蔵。                |

リポジトリには認証情報は保存されません。

## アーキテクチャの進化方法

サイトのビルド、デプロイ、自動化に影響を与える変更は、以下のことを行う必要があります：

1. 利用可能な次の番号で`memory/decisions.md`に新しいエントリとして記録される。
2. ハイレベル図を変更する場合、このページに反映される。
3. リポジトリファーストの契約を守る：公開サイトを直接編集しない。