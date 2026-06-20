---
title: Lazygit – 生産性を高めるターミナルGit UI
description: lazygitの包括的ガイドです。直感的なキーボード操作で、ステージング、リベース、コンフリクト解決などの複雑なGit操作を簡素化するターミナルベースのGit UIについて解説します。
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – 生産性を高めるターミナルGit UI

**Lazygit** は、Git用のクロスプラットフォームなキーボード駆動のTerminal User Interface（TUI）です。2018年にJesse Duffieldによって作成され、Goで書かれており、Gitの最も複雑でエラーが起こりがちな操作を、端末内に完全に収まる直感的なパネルベースのレイアウトにまとめています。

> 「Gitコマンドを暗記するのはやめよう。直感的にGitを使い始めよう。」

---

## Lazygitを選ぶ理由

Gitのコマンドラインインターフェースは強力ですが、非常に扱いにくいことで知られています。インタラクティブリベース、ハンクのステージング、コンフリクト解決、ブランチ管理などは、正確なコマンドの連続が必要です。Lazygitはこれを次のように解決します。

- **リポジトリの可視化** – ブランチ、タグ、コミットグラフ、ワーキングツリー、スタッシュを一目で確認できます。
- **日常業務の高速化** – 1つも`git`コマンドを入力せずに、ステージ、コミット、プッシュ、プルが行えます。
- **ミスの減少** – インタラクティブリベース、チェリーピック、コンフリクト解決がメニュー操作で可能になり、元に戻せます。
- **学習曲線の緩和** – 新しいチームメンバーでも、複雑な構文を覚えることなく、すぐに高度なGit操作を実行できます。
- **クロスプラットフォームでの動作** – 同じインターフェースとキーバインドで、Linux、macOS、Windowsで動作します。

---

## インストール

Lazygitはほとんどのパッケージマネージャーで利用できます。自分のプラットフォームを選んでください。

```bash
# macOS (Homebrew)
brew install lazygit

# Ubuntu / Debian
sudo add-apt-repository ppa:lazygit-team/release
sudo apt update
sudo apt install lazygit

# Arch Linux
pacman -S lazygit

# Windows
winget install lazygit
# or
scoop install lazygit

# Go (requires Go 1.16+)
go install github.com/jesseduffield/lazygit@latest

# Binary downloads (all platforms)
# https://github.com/jesseduffield/lazygit/releases
```

---

## 基本的な使い方

任意のGitリポジトリに移動して起動します。

```bash
cd my-project
lazygit
```

Lazygitは分割パネルレイアウトで開きます。左の列には（上から順に）**Status**、**Files**、**Branches**、**Commits**、**Stash**の各パネルが表示されます。右側には選択したアイテムの差分やログが表示されます。

### パネルナビゲーション

| キー | アクション |
|-----|------------|
| `←` / `→` | パネル間を移動 |
| `Tab` | パネルを順方向に循環 |
| `Shift + Tab` | パネルを逆方向に循環 |
| `j` / `k` | パネル内で上下に移動 |
| `J` / `K` | メイン差分パネルをスクロール |
| `?` | 全キーバインドヘルプを表示/非表示 |

### クイックスタート（日常ワークフロー）

1. **起動** – リポジトリ内で `lazygit` を実行。
2. **ファイルをステージ** – Filesパネルでファイルにカーソルを合わせ、`Space` を押す。
3. **特定のハンクをステージ** – `Enter` で差分を表示し、個々のハンクで `Space` を押す。
4. **コミット** – `c` を押し、メッセージを入力して `Enter` を押す。
5. **プッシュ** – `P`（大文字）を押してプッシュ。
6. **プル** – `p`（小文字）を押してプル。
7. **終了** – `q` を押して終了。

---

## 主な機能（コマンド例付き）

### 🎯 インタラクティブステージング（`git add -p` より優れている）

ファイルの差分を表示し、個々の行やハンクを視覚的にステージ/アンステージできます。もうカーソル位置を数える必要はありません。

```bash
# Inside the Files panel:
# Enter  → open the file diff
# Space  → stage the selected hunk
# a      → stage all changes
# Enter on a specific hunk → stage individual lines
```

### 🔁 インタラクティブリベース（キラー機能）

コミットの並べ替え、スカッシュ、フィックスアップ、編集、削除を単一のキー操作で行えます。

```bash
# Switch to the Commits panel (press 4):
# i       → start interactive rebase
# s       → squash commit into previous
# f       → fixup (squash, discard message)
# d       → drop commit entirely
# e       → edit commit (pause rebase)
# r       → reword commit message
# Ctrl+j  → move commit down in order
# Ctrl+k  → move commit up in order
```

マーク後、`Enter` を押して確定します。Lazygitがリベースを実行し、進行状況を表示します。コンフリクトが発生した場合は、コンフリクト解決パネルにジャンプします。

### ↩️ 元に戻す / やり直し（セーフティネット）

Lazygitは自身の内部アクション履歴を追跡します。リベース中に間違えたり、うっかりコミットを削除してしまったりしても、元に戻せます。

```bash
# z  → undo last action
# Z (Shift+z)  → redo
```

### 🌳 ブランチ管理

UIから離れることなく、ブランチの切り替え、マージ、リベース、リネーム、削除が行えます。

```bash
# Press 3 to enter the Branches panel:
# Space    → checkout selected branch
# n        → create a new branch (optionally from current HEAD)
# m        → merge selected branch into current
# r        → rebase current branch onto selected
# R        → rename branch
# d        → delete branch (with confirmation)
# Ctrl+r   → update remote branch references
```

### 🍒 コミットのチェリーピック

`git log` やコミットハッシュを探すことなく、あるブランチから別のブランチにコミットをコピーできます。

```bash
# In the Commits panel:
# c        → start cherry-pick mode
# Space    → toggle selection of a commit
# Shift+c  → complete cherry-pick
```

### 🧩 スタッシュ管理

スタッシュに名前を付け、適用し、ポップし、さらにはスタッシュからブランチを作成できます。

```bash
# Press 5 to enter the Stash panel:
# g        → toggle stash view
# s        → stash staged changes
# Shift+s  → stash all changes (including untracked files)
# Space    → apply selected stash
# d        → drop stash
# n        → name a new stash
# b        → create branch from stash
```

### ⚔️ コンフリクト解決

リベースやマージでコンフリクトが発生すると、Lazygitはインラインのコンフリクトマーカー付きの三点差分を表示します。視覚的に解決できます。

```bash
# Conflict panel will open automatically:
# Ctrl+o → open file in external merge tool
# Space  → stage resolved file
# Enter  → edit file manually
# /      → search for remaining conflict markers
```

### 🌳 ワークツリー対応

LazygitはGitワークツリーをネイティブサポートしており、追加、削除、切り替えが可能です。

```bash
# In the Branches panel (or dedicated Worktrees panel):
# w        → open worktree management
# a        → add a new worktree
# d        → remove a worktree
# Space    → switch to a worktree
```

### 🧹 カスタムコマンド

独自のシェルコマンドやスクリプトをLazygitのUIに追加して拡張できます。

```bash
# In ~/.config/lazygit/config.yml:
customCommands:
  - key: "C"
    command: "git cz"
    description: "Commit with Commitizen"
    context: "files"
    loadingText: "Opening commitizen..."
```

---

## プロのヒント

1. **Vim風のキーバインド** – `j/k` で移動、`J/K` で差分スクロール、`/` でパネル内検索。
2. **ファイルのフィルタリング** – Filesパネルで `/` を押してファイル名でフィルタリング。
3. **特定のコミットとの差分表示** – Commitsパネルでコミットにカーソルを合わせ `d` を押すと、そのコミットの変更内容を確認。
4. **差分表示の切り替え** – `Ctrl+d` で差分表示モードを切り替え。
5. **既存のGit設定を利用** – Lazygitはエイリアス、difftool、mergetoolの設定を尊重します。

---

## 設定

Lazygitは高度に設定可能です。設定ファイルは以下の場所にあります。

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

テンプレートは以下で生成できます。

```bash
lazygit --print-config
```

一般的な設定項目には、キーバインドの上書き、テーマカラー、カスタムコマンド、UIレイアウトなどがあります。

---

## Lazygitを使うべきとき

| シナリオ | Lazygitが優れている理由 |
|----------|------------------------|
| インタラクティブリベース | ビジュアルなコミット選択と並べ替え、元に戻し可能 |
| 部分的な変更のステージング | 差分を即座に確認しながら行ごと/ハンクごとに選択 |
| 新規開発者のオンボーディング | 複雑なGitコマンドを覚える必要なし |
| コードレビューの準備 | 数分でクリーンで論理的なコミット系列を作成 |
| コンフリクト解決 | インラインアクション付き三点差分ビューア |
| リポジトリの概要把握 | ブランチ、タグ、リモート、スタッシュ、コミットグラフを一覧表示 |

---

## リソース

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **ドキュメント:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **設定リファレンス:** [lazygit Configuration](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **作者の「lazy」エコシステム:** Lazygit、Lazydocker、Lazynpm – すべて同じTUI哲学に従っています。

---

LazygitはGitを置き換えるものではありません。Gitをよりアクセスしやすく、視覚的で、高速なものにします。Gitの熟練ユーザーでも、コードを書くことに集中したい開発者でも、Lazygitは毎週何時間も節約してくれるでしょう。一度使ってみてください — もう普通の `git rebase -i` には戻れなくなります。