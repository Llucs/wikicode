---
title: Postman - API開発・テストプラットフォーム
description: APIの設計、構築、テスト、ドキュメント化のための業界標準プラットフォームであるPostmanの包括的ガイド。
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - API開発・テストプラットフォーム

## Postmanとは？

Postmanは、APIライフサイクルの各ステップ（設計、開発、テスト、ドキュメント化、モニタリング）を簡素化する完全なAPIプラットフォームです。当初はシンプルなHTTPクライアントとして始まりましたが、現在では世界中の何百万人もの開発者やQAエンジニアが利用するコラボレーション環境に進化しています。PostmanはREST、GraphQL、SOAPプロトコルをサポートし、APIを効率的に構築・操作するための豊富なツールセットを提供します。

## Postmanを使う理由

- **包括的なHTTPクライアント:** 任意のメソッドのリクエストを簡単に送信し、ヘッダー、認証、ボディコンテンツをカスタマイズできます。
- **組織化ツール:** リクエストをコレクションにグループ化し、環境で変数を管理し、ワークスペース全体でデータを再利用できます。
- **スクリプティング＆テスト:** JavaScriptテストスクリプトを作成してアサーションを自動化し、リクエスト間でデータを抽出し、動的なワークフローを処理できます。
- **自動化対応:** Collection Runnerによる手動実行、またはNewmanによるヘッドレス実行（CI/CD、パイプライン）が可能です。
- **コラボレーション:** バージョン管理とコメント機能を備えたクラウドワークスペースを介してコレクションと環境を共有できます。
- **ドキュメント＆モッキング:** APIドキュメントを自動生成し、バックエンドが準備できる前にAPIレスポンスをシミュレートするモックサーバーを作成できます。
- **モニタリング:** モニターを設定してコレクションの実行をスケジュールし、APIの健全性を確認できます。

## インストール

### デスクトップアプリ（推奨）

PostmanはWindows、macOS、Linux向けのネイティブデスクトップアプリを提供しています。

- [getpostman.com](https://getpostman.com) から適切なインストーラーをダウンロードしてください。
- または、**Webバージョン**を [go.postman.co](https://go.postman.co) で使用し、Desktop Agentを介してAPI呼び出しを処理することもできます。

### Newman（CI/CD用CLI）

NewmanはPostmanのコマンドラインコレクションランナーです。コマンドラインから直接Postmanコレクションを実行およびテストできるため、APIテストを開発パイプラインに統合するのに最適です。

npmでインストール:

```bash
npm install -g newman
```

またはYarnで:

```bash
yarn global add newman
```

## 基本的な使い方

1. **リクエストを作成する**  
   **New** ボタンをクリックして **HTTP Request** を選択します（または `Ctrl+N` を使用）。

2. **リクエストを指定する**  
   - URLを入力します（例: `https://jsonplaceholder.typicode.com/posts`）  
   - HTTPメソッド（`GET`、`POST`、`PUT`など）を選択します  
   - 必要なヘッダー、クエリパラメーター、リクエストボディを追加します。

3. **送信して確認する**  
   **Send** をクリックします。レスポンスペインにステータスコード、応答時間、ヘッダー、ボディが表示されます。

4. **コレクションに保存する**  
   **Save** をクリックし、新しいコレクションを作成するか、既存のコレクションに追加します。

5. **テストを追加する**  
   **Tests** タブで、レスポンスを検証するJavaScriptスクリプトを記述します。例:

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   リクエストを再実行すると、テスト結果が **Test Results** タブに表示されます。

## 主な機能と例

### 1. コレクション

コレクションを使用すると、関連するリクエストをグループ化し、チームと共有できます。コレクションにはフォルダやメタデータを含めることもできます。

```javascript
// プリリクエストスクリプトでコレクション変数を使用する例
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

Newmanを使用してコレクション全体を実行:

```bash
newman run MyCollection.json
```

### 2. 環境

環境には、セットアップ（開発、ステージング、本番）間で変更される変数のキーと値のペアが含まれます。

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

リクエストURLで `{{base_url}}` を使用します。環境を切り替えることで、コンテキストを即座に変更できます。

### 3. プリリクエストスクリプトとテストスクリプト

PostmanスクリプトはJavaScriptで記述され、`pm` などのPostman提供オブジェクトにアクセス可能なサンドボックスで実行されます。

**プリリクエストスクリプト**（リクエスト送信前に実行）:

```javascript
// タイムスタンプパラメータを動的に設定
pm.variables.set("timestamp", Date.now());
```

**テストスクリプト**（レスポンス受信後に実行）:

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. Collection Runner

データファイルを使用して、コレクションまたはフォルダ全体を複数回実行できます。

- Postman左上の **Runner** を開きます。
- コレクションを選択し、環境を選び、反復回数を設定します。
- CSVまたはJSONデータファイルを提供して、各反復にデータを注入できます。

### 5. Newman – コマンドライン統合

Newmanを使用すると、PostmanテストをCI/CDパイプライン（Jenkins、GitLab CI、GitHub Actionsなど）に統合できます。

**環境とデータファイルを指定してコレクションを実行:**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

`htmlextra` レポーターは、テスト実行のインタラクティブなHTMLレポートを生成します。

**Node.jsスクリプトでの使用:**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. ドキュメント生成

Postmanは、任意のコレクションのドキュメントを自動生成できます。コレクションを開き、**...** メニューをクリックして **View documentation** を選択するだけです。ドキュメントには、リクエスト例、リクエスト/レスポンススキーマ、さまざまな言語でのコードスニペットが含まれます。

**Publish Docs** ボタンでドキュメントをWebに公開するか、HTMLとしてエクスポートします。

### 7. モックサーバー

コレクションからモックサーバーを作成してAPIを模倣します。これは、バックエンドがまだ準備できていない場合のフロントエンド開発に非常に役立ちます。

- コレクションを選択し、**Mock Servers** をクリックします。
- Postmanが、保存されたサンプルレスポンスを返すモックサーバーURLを作成します。

### 8. モニター

モニターを使用すると、Postmanのクラウドインフラストラクチャ上でコレクションの定期的な実行をスケジュールできます。テストが失敗した場合にアラートを受け取ることができます。

- **Monitors** → **Create a monitor** に進みます。
- コレクションを選択し、頻度（例: 毎時）を設定し、必要に応じてアラート（メール、Slackなど）を定義します。

## まとめ

Postmanは単なるAPIクライアント以上のものです。APIライフサイクル全体をサポートする本格的なプラットフォームです。初期のモッキングや共同設計から、Newmanによる自動テスト、本番モニタリングまで、PostmanはチームにAPIの唯一の情報源を提供します。使いやすさと強力なスクリプト機能、CI/CD統合を兼ね備えたPostmanは、現代の開発ワークフローに不可欠なツールです。