---
title: ガイド
description: 長編のトピック指向のガイド。
created: 2026-06-03
tags:
  - meta
status: stable
---

# ガイド

トピックごとにグループ化された長編ガイドです。各ガイドは `docs/guides/` (またはサブフォルダ) 内の実際の Markdown ファイルです。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新日: 自動 (git)</span>
</div>

## 表記規則

- ガイドごとに1つのフォルダまたは `.md` ファイル。
- フォルダ名は小文字、ハイフン区切り。
- フロントマターには `title`、`description`、`created`、`tags` を含める必要があります。
- タグはクロスリンクに役立ちます: 新しいタグを作成するよりも、[タグ](../tags.md) の既存のタグを再利用することを推奨します。

## 推奨タグ

| タグ             | 意味                                                  |
| --------------- | -------------------------------------------------------- |
| `meta`          | WikiCode 自体についてのページ。                             |
| `guide`         | ハウツーコンテンツ。                                          |
| `reference`     | リファレンス資料 (用語集、リスト)。                  |
| `architecture`  | Wiki の構築方法と動作方法。                  |
| `process`       | ワークフロー、コントリビューション、ガバナンス。                     |
| `language-go`   | 主に Go に関するコンテンツ。                              |
| `language-py`   | 主に Python に関するコンテンツ。                          |
| `language-cpp`  | 主に C++ に関するコンテンツ。                             |
| `language-rs`   | 主に Rust に関するコンテンツ。                            |
| `language-js`   | 主に JavaScript / TypeScript に関するコンテンツ。        |
| `backend`       | バックエンドエンジニアリングのトピック。                             |
| `frontend`      | フロントエンドエンジニアリングのトピック。                            |
| `devops`        | ビルド、デプロイ、オブザーバビリティ。                            |
| `security`      | セキュリティのトピック。                                         |
| `data`          | データベース、パイプライン、アナリティクス。                         |

以下のようにフロントマターにタグを追加します:

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```