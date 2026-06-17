---
title: Visual Studio Code
description: Microsoft が開発した、軽量でありながら強力なソースコードエディター。統合開発ツールとして機能します。
created: 2026-06-14
tags:
  - editor
  - development
  - microsoft
  - open-source
status: draft
ecosystem: editors
---

# Visual Studio Code

## VS Code とは

Visual Studio Code (一般に VS Code と呼ばれます) は、Microsoft が開発した無料のオープンソースソースコードエディターです。Electron フレームワーク上に構築されており、Windows、macOS、Linux で動作します。VS Code は、軽量エディターの速度とシンプルさを、豊富な拡張機能アーキテクチャを通じて統合開発環境 (IDE) の高度な機能と組み合わせています。

## VS Code が選ばれる理由

- **パフォーマンス**: 起動が速く、大規模なプロジェクトでも応答性を維持します。
- **拡張性**: 数千もの拡張機能が、言語、テーマ、デバッガー、ワークフローツールを追加します。
- **クロスプラットフォーム**: 主要なオペレーティングシステムすべてで同じエクスペリエンスを提供します。
- **統合ツール**: Git 管理、ターミナル、デバッグ – すべてエディター内で完結します。
- **インテリジェントな編集**: IntelliSense がコンテキストに応じた補完、パラメーター情報、ドキュメントを提供します。
- **モダンなワークフローへの組み込みサポート**: Docker、リモート開発、Jupyter Notebook などに対応。

## インストール

### インストーラーのダウンロード
最も簡単な方法は、[公式 Web サイト](https://code.visualstudio.com) からインストーラーをダウンロードすることです。

| プラットフォーム | インストーラーの種類 |
|----------|----------------|
| Windows  | `.exe` (ユーザーまたはシステム) |
| macOS    | `.dmg` (アプリケーションフォルダにドラッグ) |
| Linux    | `.deb` (Debian/Ubuntu) または `.rpm` (Fedora/RHEL) |

### パッケージマネージャー

**macOS (Homebrew)**
```bash
brew install --cask visual-studio-code
```

**Linux (Snap)**
```bash
snap install code --classic
```

**Windows (winget)**
```bash
winget install Microsoft.VisualStudioCode
```

### ポータブルモード
VS Code 実行ファイルと同じディレクトリに `data` フォルダーを作成します。エディターはすべての設定、拡張機能、ユーザーデータをそのフォルダー内に保存し、完全にポータブルになります。

### Insiders ビルド
機能への早期アクセスや毎日のビルドを利用するには、[VS Code Insiders](https://code.visualstudio.com/insiders) をインストールしてください。安定版とサイドバイサイドでインストールできます。

## 基本的な使い方

### プロジェクトを開く
VS Code を起動し、**ファイル → フォルダーを開く** (または `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`) でプロジェクトディレクトリを開きます。

### コマンドパレット
コマンドパレットを使用すると、VS Code のすべての操作にアクセスできます。

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

よく使うコマンド: `>ドキュメントのフォーマット`, `>基本設定: 設定を開く`, `>拡張機能: 拡張機能のインストール`。

### ファイルの編集
- シンタックスハイライトはファイル拡張子に基づいて自動的に行われます。
- **マルチカーソル**: `Alt+クリック` (Windows/Linux) または `Option+クリック` (macOS) でカーソルを追加。
- **括弧の対応**: 括弧内にカーソルを移動すると、対応する括弧が強調表示されます。
- **IntelliSense**: `Ctrl+Space` で手動でトリガーできます。

### バージョン管理
ソース管理ビュー (`Ctrl+Shift+G` (Windows/Linux)、`Cmd+Shift+G` (macOS)) を開いて、変更の確認、ファイルのステージ、コミット、プッシュ/プルを行います。より複雑な操作には組み込みターミナルを使用します。

### 統合ターミナル
`` Ctrl+` `` (バッククォート) でターミナルを起動します。ターミナルはデフォルトでシステムシェル (PowerShell、bash、zsh など) を使用します。

### 拡張機能
`Ctrl+Shift+X` で拡張機能ビューを開きます。任意の拡張機能 (例：「Python」、「Prettier」、「Docker」) を検索し、ワンクリックでインストールできます。

### デバッグ
ガター (行番号領域) をクリックするか `F9` を押してブレークポイントを設定します。`F5` を押して、現在アクティブな設定でデバッグを開始します。`launch.json` ファイルを作成して、プロジェクトのデバッグ設定を構成します。

## 主な機能とコマンド例

### IntelliSense
VS Code は、言語サービス、変数型、関数定義に基づいてスマートな補完を提供します。

```javascript
// 例: "console." と入力後、Ctrl+Space で log、warn、error などのメソッドが表示される
console.log("Hello, VS Code!");
```

**IntelliSense の手動トリガー**: `Ctrl+Space` (Windows/Linux) または `Cmd+Space` (macOS)。

**パラメーターヒント**: 関数呼び出し時に、VS Code が期待されるパラメーターを表示します。

### 統合デバッグ
起動構成による完全なデバッグサポート。

**Node.js 用の launch.json 例:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/app.js"
        }
    ]
}
```

**主なデバッグコマンド:**
| アクション | キー |
|--------|------|
| 開始/続行 | `F5` |
| ステップオーバー | `F10` |
| ステップイン | `F11` |
| ステップアウト | `Shift+F11` |
| ブレークポイントの切り替え | `F9` |

### 組み込み Git
ステージ、コミット、ブランチなどを備えたビジュアルソース管理。

**コマンドパレットでの同等操作:**
- `>Git: Commit` – ステージされた変更をコミット。
- `>Git: Create Branch` – 新しいブランチを作成。
- `>Git: Clone` – リモートリポジトリをクローン。
- `>Git: Pull` / `Git: Push` – 変更を同期。

### 拡張機能マーケットプレイス
拡張機能をインストールして、言語、リンター、テーマ、スニペット、デバッガーを追加します。

**例: Python 拡張機能のインストール**
1. 拡張機能ビューを開く (`Ctrl+Shift+X`)。
2. 「Python」(by Microsoft) を検索。
3. **インストール** をクリック。

**人気の拡張機能:**
- Python
- Prettier – Code formatter
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### 統合ターミナル
VS Code から離れずにシェルコマンドを実行。

```bash
# 例: 統合ターミナル内で
npm install && npm start
```

`` Ctrl+` `` でターミナルの開閉。複数のターミナルを作成可能 (例: ビルド用、Git 用)。

### リモート開発
以下のようなリモート環境に接続:
- **WSL** (Windows Subsystem for Linux)
- **SSH** リモートマシン
- **Dev Containers** (Docker)
- **GitHub Codespaces**

**コマンドパレットの例:**
- `>Remote-SSH: ホストに接続...`
- `>Dev Containers: コンテナーで再度開く`

エディターを離れる必要はありません。開発環境全体にローカルでアクセスできます。

## 追加のヒント

### 設定の同期
Microsoft アカウントまたは GitHub アカウントでサインインすると、設定、キーバインド、拡張機能が複数のマシン間で同期されます。

**コマンドパレット**: `>設定の同期を有効にする...`

### スニペット
繰り返しパターン用のカスタムコードスニペットを作成。

**ファイル → 基本設定 → ユーザースニペットの構成** → 言語を選択。

```json
// JavaScript スニペット例 (javascript.json 内)
{
    "Arrow Function": {
        "prefix": "arr",
        "body": ["const ${1:name} = (${2:params}) => {", "\t${3:body}", "};"],
        "description": "アロー関数を作成する"
    }
}
```

### マルチカーソル編集
- `Alt+クリック` – カーソルを追加。
- `Ctrl+Alt+↑/↓` – カーソルを上/下に挿入。
- `Ctrl+D` – 現在の選択範囲の次の出現箇所を選択。

### Zen モード
コードに集中: `Ctrl+K Z` (Windows/Linux) または `Cmd+K Z` (macOS)。`Esc Esc` で解除。

## まとめ

Visual Studio Code は、速度、パワー、カスタマイズ性のバランスが取れた多用途エディターです。IntelliSense、デバッグ、Git 統合、ターミナル、拡張機能エコシステムといった中核機能を習得することで、言語やプラットフォームを問わず開発ワークフローを効率化できます。

さらに詳しく学ぶには、[公式 VS Code ドキュメント](https://code.visualstudio.com/docs) を参照してください。