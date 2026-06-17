---
title: はじめに
description: リポジトリの構成、ローカルビルド、およびコントリビューションの規約。
created: 2026-06-03
---

# はじめに

WikiCode を読み、ビルドし、貢献するために必要なすべて。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新日: 自動 (git)</span>
</div>

## 1. リポジトリ構成

```
.
├── README.md            # Project overview
├── LICENSE              # MIT License
├── AGENT.md             # Operating contract for agents
├── mkdocs.yml           # Static site configuration
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # Builds and deploys the site on push to main
│       └── wikicode-agent.yml# Autonomous agent workflow
├── docs/                # Site content (articles, guides)
│   ├── assets/css/      # Custom styling
│   ├── index.md
│   └── getting-started.md
├── projects/            # Self-contained developer projects
├── snippets/            # Reusable code snippets
├── memory/              # Long-term agent memory
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # Work pipeline
│   ├── queue.md
│   └── completed.md
└── reports/             # Time-stamped execution reports
```

## 2. 「Wiki はリポジトリから成長する」ループ

WikiCode は **リポジトリファースト** のサイトです。`site/`（公開アウトプット）内のものは手作業で編集されません。

1. リポジトリに変更が加えられます（新しい記事、プロジェクト、スニペット、レポート、決定など）。
2. 変更がコミットされ、`main` にプッシュされます。
3. プッシュ時に `.github/workflows/pages.yml` が自動的に実行されます。
4. MkDocs が `docs/`、`projects/`、`snippets/` を読み取り、サイト全体を再構築します。
5. GitHub Pages が新しいビルドを公開します。

ローカル AI エージェント（または任意のコントリビューター）は、リポジトリに書き込むことでこのループに参加します。サイトは手動操作なしで変更を反映します。

## 3. サイトをローカルで実行する

Python 3.10 以降が必要です。

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

サイトは `http://127.0.0.1:8000` で利用できます。`docs/`、`projects/`、または `snippets/` 以下の Markdown ファイルを編集すると、即座にリロードがトリガーされます。

## 4. 静的サイトをビルドする

```bash
mkdocs build --clean
```

出力は `site/` に書き込まれます。CI でも同じコマンドが使用されます。

## 5. コンテンツの追加

| 追加したいもの | 配置場所                              | 必要なファイル                      |
| -------------- | ------------------------------------- | ----------------------------------- |
| 記事           | `docs/<topic>/<slug>.md` または `docs/` | `.md` ファイル自体               |
| プロジェクト   | `projects/<slug>/`                     | `README.md` + `index.md` + ソース   |
| スニペット     | `snippets/<slug>/`                     | コードファイル + `index.md`          |
| 決定           | `memory/decisions.md`                  | 新しいエントリを追加                |
| タスク         | `tasks/queue.md`                       | 新しいチェックボックスエントリを追加 |
| レポート       | `reports/YYYY-MM-DD-<slug>.md`         | ファイル + インデックス更新         |

`docs/` に含まれないセクション（プロジェクト、スニペット）は、`index.md` ファイルを通じて `awesome-pages` MkDocs プラグインによって自動的に認識されます。

## 6. フロントマター

サイト上のすべてのページは、少なくとも以下を持ちます。

```yaml
---
title: Page title
description: Short description.
created: YYYY-MM-DD
---
```

`created` の日付は、ページが最初に追加されたときに設定されます。**最終更新日**はファイルの git 履歴から自動的に取得されるため、手動編集なしで常に正確です。

## 7. 自律的に作業する

エージェントは `AGENT.md` に従う必要があります。短いバージョン:

1. `memory/mission.md` と `memory/rules.md` を読む。
2. `tasks/queue.md` から次のタスクを選ぶ。
3. リポジトリに意味のある変更を1つだけ行う。
4. `reports/` にレポートを書く。
5. タスクを `tasks/completed.md` に移動する。
6. コミットしてプッシュする。サイトは自動的に再構築されます。

## 8. 検索

WikiCode は完全に検索可能です。検索インデックスはデプロイ時に構築され、ブラウザ内で完全に動作します。

- 任意のページで ++slash++ を押すと検索バーにフォーカスします。
- インデックスはサイト上のすべてのページをカバーし、コードブロックやブログ投稿も含まれます。
- 詳細とヒントについては、[検索](search.md)を参照してください。

## 9. エージェントのトリガー方法

wikicode-agent ワークフローは **自動と手動の両方** のトリガーをサポートしています:

| トリガー              | タイミング                              | ユースケース                                  |
| --------------------- | --------------------------------------- | --------------------------------------------- |
| `schedule`            | 毎日 12:00 UTC                          | デフォルトの「毎日少しずつ成長」実行。        |
| `workflow_dispatch`   | Actions タブから手動                    | オンデマンド実行、ブロック解除に便利。        |
| `issue_comment`       | 誰かが Issue に `@agent` を書いたとき   | Issue をコントリビューションに変換。          |
| `issues` とラベル     | Issue に `agent` ラベルが付けられたとき | オペレーターが厳選したバッチ実行。            |

実行ごとに **1 つ** のタスクのみが実行されます。AI はコンテンツ生成に OpenCode API を使用します — 外部 API キーは不要です。

## 10. 規約

- Markdown ファイル名: 小文字、ハイフン区切り。
- すべてのプロジェクト、スニペット、ツールフォルダはナビゲーション用に `index.md` を公開します。
- アーキテクチャ、ツール、ワークフローに関する決定は `memory/decisions.md` に記録されます。
- 認証情報、トークン、プライベートデータは決してコミットされません。
- ローカル AI エージェントは `secrets.GITHUB_TOKEN`（組み込み）を使用してコミットおよびプッシュします。外部 API キーは必要ありません。