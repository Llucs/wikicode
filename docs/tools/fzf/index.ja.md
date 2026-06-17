---
title: fzf - コマンドライン用ファジーファインダー
description: 端末でのファイルおよびテキスト検索を強化するコマンドライン用ファジーファインダーツールです。
created: 2026-06-15
tags:
  - command-line
  - fuzzy-finder
  - fzf
  - productivity
  - terminal
status: draft
ecosystem: cli
---

# fzf – 汎用コマンドライン用ファジーファインダー

fzf はインタラクティブな **ファジーファインダー** であり、コマンドライン上に表示された任意のリストに対してインクリメンタル検索の力を提供します。もともとは [Junegunn Choi](https://github.com/junegunn) によって Ruby で書かれ、後に Go で書き直されました。今では、ファイル、コマンド、プロセスなどを驚くべき速さで操作したい開発者、システム管理者、パワーユーザーにとって不可欠なツールとなっています。

正確な名前を入力したり、タブ補完だけに依存する代わりに、fzf は任意のサブストリング（またはファジーシーケンス）を入力するだけで、即座に入力をフィルタリングします。stdin からストリームされる任意のデータで動作し、選択したアイテムを stdout に返すため、Unix パイプラインに最適です。

---

## fzf を使う理由

- **速度**: 数十万のエントリをほぼリアルタイムで処理します。
- **ファジーマッチング**: 正確な名前を覚えていなくてもファイルやコマンドを見つけられます。
- **インタラクティブ性**: リアルタイムのフィルタリングと即時の視覚的フィードバック。
- **構成可能性**: テキストを生成または消費する任意のコマンドで動作します。
- **カスタマイズ性**: テーマ、キーバインド、プレビューウィンドウなど。

---

## インストール

### macOS
```bash
brew install fzf
# Install useful key bindings and fuzzy auto-completion
$(brew --prefix)/opt/fzf/install
```

### Linux (Debian/Ubuntu)
```bash
sudo apt install fzf           # Often outdated – prefer building from source
# Or from the official repository:
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Arch Linux
```bash
sudo pacman -S fzf
```

### Windows (WSL / Git Bash / Scoop)
```bash
scoop install fzf
# Or with Chocolatey
choco install fzf
```

### Go (全プラットフォーム)
```bash
go install github.com/junegunn/fzf@latest
```

---

## 基本的な使い方

### リストをパイプで fzf に渡す
```bash
# カレントディレクトリ内のすべてのファイルを検索
find . -type f | fzf
```

### ファイルを選択してエディタで開く
```bash
vim "$(find . -type f | fzf)"
```

### ファイル内容のプレビュー
```bash
fzf --preview 'cat {}'       # {} は現在のアイテムのパス
```

### レイアウトを反転（検索を下部に表示）
```bash
fzf --reverse
```

### 複数選択（Tab キー使用）
```bash
fzf --multi
```

### カスタムプロンプト
```bash
fzf --prompt="ファイルを選んでください> "
```

---

## 主な機能

### ファジーマッチングモード
fzf は検索を微調整するためのいくつかのマッチングモードをサポートしています：

- **ファジー（デフォルト）**: `abc` は `alphabet.txt` にマッチします – 任意のサブストリングシーケンスが動作します。
- **完全一致**: プレフィックスに `'` を付ける → `'abc` は「abc」を正確に含む行のみにマッチします。
- **前方一致**: サフィックスに `^` を付ける → `^abc` は「abc」で始まる行にマッチします。
- **後方一致**: プレフィックスに `$` を付ける → `abc$` は「abc」で終わる行にマッチします。
- **正規表現**: `!` プレフィックスで反転、または `rg` の統合を使用。

### プレビューウィンドウ
プレビューウィンドウはハイライトされたアイテムのコンテキスト情報を表示します。`cat`、`bat`、`head`、またはカスタムスクリプトなどの外部コマンドを使用できます：

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### シェル統合
公式の `install` スクリプトは、3つの便利なキーバインド（Bash、Zsh、Fish）を設定します：

| ショートカット | アクション |
|----------|--------|
| `Ctrl+R` | コマンド履歴を検索 |
| `Ctrl+T` | ファイル/ディレクトリを検索してパスを貼り付け |
| `Alt+C`  | サブディレクトリにジャンプ（ファジーcd） |

### Vim / Neovim プラグイン
fzf はネイティブの Vim プラグインを提供しています。最も人気のある拡張は [fzf.vim](https://github.com/junegunn/fzf.vim) で、次のようなコマンドを追加します：

| コマンド | 目的 |
|---------|---------|
| `:Files [パス]` | ファイルを検索 |
| `:Rg [パターン]` | ファイル内容を検索（ripgrep が必要） |
| `:Buffers` | 開いているバッファを切り替え |
| `:GFiles?` | Git リポジトリ内の追跡されていないファイルを検索 |
| `:Commands` | Vim コマンドを一覧表示 |
| `:Maps` | キーマッピングを表示 |

### 拡張性
fzf は stdin/stdout で動作するため、あらゆるワークフローにシームレスに統合できます。シェル関数やスクリプトでラップして、独自のインタラクティブメニューを作成できます。

---

## 高度なユースケース

### プロセスキラー
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### Git ブランチのチェックアウト
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### 設定から SSH ホストに接続
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### プレビュー付きファイル内容検索
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### インタラクティブなディレクトリ移動（fd を使用）
```bash
cd "$(fd --type d | fzf)"
```
または組み込みの `Alt+C` バインディングを使用。

### Docker コンテナ検索
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## ヒントとコツ

- **`--header` オプション** を使って説明を表示：
  ```bash
  fzf --header "Ctrl+R で履歴、Ctrl+T でファイルを検索"
  ```
- **選択したアイテムを変数に格納** してバッチ操作に利用。
- **カラープレビュー** は `bat` や `highlight` を ANSI 対応で使用。
- **tmux と組み合わせて** プレビューを別ペインで表示。
- **カラースキームのカスタマイズ** は `FZF_DEFAULT_OPTS` 環境変数で：
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## まとめ

fzf はインタラクティブなターミナル検索におけるゴールドスタンダードツールです。そのファジーマッチング、速度、構成可能性は、コマンドラインで作業するすべての人にとって不可欠なものにしています。ファイルの閲覧、プロセスの追跡、カスタムワークフローの構築など、fzf は面倒な検索作業を流動的でほとんど魔法のような体験に変えます。

詳細なドキュメントは、[GitHub リポジトリ](https://github.com/junegunn/fzf) をご覧ください。