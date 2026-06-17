---
title: npm - Node Package Manager
description: Node.js向けのパッケージマネージャーで、JavaScriptの依存関係を管理するための基本的なツールです。
created: 2026-06-14
tags:
  - package-manager
  - javascript
  - nodejs
  - cli
  - dependency-management
status: draft
ecosystem: javascript
---

# npm – Node Package Manager

npm（Node Package Manager）は、Node.js JavaScriptランタイムのデフォルトパッケージマネージャーです。これは主に2つのコンポーネントから構成されています：依存関係を管理するための**CLI**（コマンドラインインターフェース）と、JavaScriptパッケージの大規模な公開データベースである**npm Registry**です。これはJavaScriptエコシステムにおいて不可欠なツールとなり、開発者がコードを効率的に共有、再利用、管理することを可能にします。

## npmとは？

npmは以下の機能を提供します：

- **依存関係のインストールと管理** – `package.json`やロックファイルでパッケージを追跡します。
- **パッケージの公開** – 自身のライブラリをコミュニティや組織と共有します。
- **スクリプトの実行** – ビルド、テスト、デプロイのワークフローを自動化します。
- **モノレポの管理** – ワークスペースを使用して単一リポジトリ内で複数のパッケージを管理します。

## npmを使う理由

- **標準化** – npmはNode.jsにバンドルされており、ほとんどのJavaScriptプロジェクトでのデフォルトの選択肢となっています。
- **巨大なエコシステム** – レジストリには200万以上のパッケージがあり、ほぼすべてのニーズをカバーしています。
- **再現性** – `package-lock.json`ファイルにより、環境間で決定論的なインストールが保証されます。
- **セキュリティ** – `npm audit`で依存関係ツリーの脆弱性を発見し修正できます。
- **利便性** – `npx`を使用するとグローバルインストールなしでパッケージを実行でき、スクリプトによって一般的なタスクが簡素化されます。

## インストール

npmはNode.jsとともに自動的にインストールされます。最新のLTSバージョンを入手するには：

1. [nodejs.org](https://nodejs.org/)からNode.jsをダウンロードします。
2. インストールを確認します：

```bash
node -v
npm -v
```

### バージョンマネージャー（nvm/fnm）を介したインストール

バージョンマネージャーを使用すると、Node.jsのバージョンを切り替え、それぞれにnpmをインストールできます：

```bash
# Example with nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

インストール後、npmが使用可能になります。

## 基本的な使い方

### プロジェクトの初期化

新しいプロジェクトを作成するか、既存のフォルダを変換します：

```bash
npm init -y
```

これにより、デフォルト値で`package.json`ファイルが生成されます。インタラクティブなプロンプトを使用するには、`npm init`（`-y`なし）を使用します。

### 依存関係のインストール

```bash
# Production dependency
npm install lodash

# Dev-only dependency
npm install --save-dev jest

# Global package (use sparingly; prefer npx)
npm install -g nodemon

# Install all dependencies from package.json
npm install
```

### 特定のバージョンのインストール

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### スクリプトの実行

スクリプトは`package.json`の`"scripts"`キーで定義されます。一般的なショートカット：

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### パッケージのアンインストール

```bash
npm uninstall lodash
```

### パッケージの更新

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### 脆弱性の確認

```bash
npm audit
```

自動修正するには（可能な場合）：

```bash
npm audit fix
```

### CIのためのクリーンインストール

```bash
npm ci
```

`npm ci`は高速で、`package-lock.json`から正確にインストールする前に`node_modules`を削除します。

## 主な機能

### npx – インストールせずにパッケージを実行

`npx`はnpmに付属しており、グローバルインストールなしでレジストリからバイナリを実行できます：

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

パッケージがすでにローカルにインストールされている場合、`npx`はそのバージョンを使用します。

### ワークスペース（モノレポサポート）

npmワークスペースを使用すると、単一のリポジトリで複数のパッケージを管理できます：

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

その後、すべてのワークスペースに対してコマンドを実行します：

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

ワークスペースパッケージ間のリンクは自動的に処理されます。

### スクリプトのライフサイクルフック

npmは一般的なスクリプトに対してpre/postフックを提供します：

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

例：

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

このファイルは、すべての依存関係とその推移的依存関係の正確なバージョンをロックします。これにより、`npm install`を実行する全員が同じツリーを取得し、ビルドが再現可能になります。

### オーバーライドと解決

`package.json`で推移的依存関係の特定のバージョンを強制できます：

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

これは、サブ依存関係に脆弱性があり、親のリリースを待たずにパッチを適用する必要がある場合に便利です。

### npm config

グローバルまたはプロジェクトごとにnpmの動作をカスタマイズします：

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

プロジェクトルートに`.npmrc`ファイルを使用することもできます。

### グローバルパッケージとnpxの比較

グローバルインストールは、複数のプロジェクトで使用するツール（例：`npm`、`yarn`、`node-gyp`）に限定する必要があります。単発のコマンドには`npx`を優先して使用し、グローバル名前空間を汚染せず、常に意図したバージョンを使用できるようにします。

## 結論

npmは、あらゆるJavaScript開発者にとって強力で不可欠なツールです。シンプルな依存関係のインストールから複雑なモノレポ管理まで、その豊富な機能セットはプロジェクトを整理された状態、安全で再現可能な状態に保つのに役立ちます。小さなライブラリから大規模なアプリケーションまで、npmを使いこなすことでワークフローが大幅に改善されます。