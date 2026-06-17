---
title: 用語集
description: WikiCode全体で使用される用語。
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# 用語集

WikiCode全体で使用される標準的な用語。定義は簡潔で、必要に応じて信頼できるソースにリンクしています。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新: 自動 (git)</span>
</div>

## 基本概念

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>リポジトリとそれが生成する静的サイトです。"WikiCode" は文脈に応じてその両方を指します。</dd>

<dt markdown>**Article**</dt>
<dd markdown>`docs/` にある長文のMarkdownページです。記事は全文読まれることを意図しています。</dd>

<dt markdown>**Project**</dt>
<dd markdown>`projects/` にある、自己完結した実行可能なソフトウェアです。各プロジェクトには独自の `README.md`、`index.md`、ソースツリーがあります。</dd>

<dt markdown>**Snippet**</dt>
<dd markdown>`snippets/` にある、小規模で焦点を絞った実行可能なコードユニットです。スニペットはコピーして適応することを意図しています。</dd>

<dt markdown>**Report**</dt>
<dd markdown>`reports/` にあるタイムスタンプ付きのMarkdownファイルで、1回の実行を説明します。形式: `YYYY-MM-DD-<slug>.md`。</dd>

<dt markdown>**Decision**</dt>
<dd markdown>`memory/decisions.md` に記録された、4桁の番号とステータスを持つアーキテクチャまたは運用上の選択です。</dd>

<dt markdown>**Agent**</dt>
<dd markdown>リポジトリで作業する際に `AGENT.md` に従う、人間または自律的なプロセスです。</dd>

<dt markdown>**Task**</dt>
<dd markdown>`tasks/queue.md` にリストされた単一の作業単位です。実行ごとに1つのタスクです。</dd>
</dl>

## ワークフロー用語

<dl markdown>
<dt markdown>**Push to `main`**</dt>
<dd markdown>`pages.yml` をトリガーし、サイトを再構築してデプロイします。公開サイトへのすべての変更はこのメカニズムを介して行われます。</dd>

<dt markdown>**Agent run**</dt>
<dd markdown>`.github/workflows/wikicode-agent.yml` のトリガー実行であり、`workflow_dispatch`、Issueでの`@agent`メンション、または`agent`ラベルが付けられたIssueによって行われます。</dd>

<dt markdown>**Frontmatter**</dt>
<dd markdown>Markdownファイルの先頭にあるYAMLメタデータで、`---` で区切られます。WikiCodeは少なくとも `title`、`description`、`created` を必要とします。</dd>

<dt markdown>**Tag**</dt>
<dd markdown>フロントマターで宣言されたラベルで、関連するページをグループ化します。Materialはタグごとのインデックスページを自動的にレンダリングします。</dd>
</dl>

## ステータス値

ページとプロジェクトはフロントマターで `status` を宣言できます:

| ステータス      | 意味                                                         |
| ----------- | --------------------------------------------------------------- |
| `draft`     | 作業中; 不完全または間違っている可能性があります。                   |
| `stable`    | レビュー済みで正しいと見なされます。まだ進化する可能性があります。              |
| `archived`  | 参照用に保持; もはやメンテナンスされていません。                      |
| `deprecated`| 他のものに取って代わられました; 歴史的文脈のために保持されています。      |

`status: stable` は公開されたコンテンツのデフォルトの期待値です。