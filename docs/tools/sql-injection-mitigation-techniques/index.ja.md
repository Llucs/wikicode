---
title: SQL注入対策技術
description: ウェブアプリケーションインターフェースを通じて悪意のあるSQLステートメントを挿入するのを防ぐための技術。パラメータクエリ、入力検証、データベース構成のセキュリティを使用する。
created: 2026-07-22
tags:
  - セキュリティ
  - ウェブアプリケーション
  - データベース
  - SQL
status: 草稿
---

# SQL注入対策技術

SQL注入は、攻撃者がウェブアプリケーションの入力フィールドに悪意のあるSQLステートメントを挿入することで、不正なアクセス、データ漏洩、さらにはデータベースサーバーの完全制御を可能にするタイプのサイバーアタックです。このドキュメントでは、SQL注入脆弱性を軽減するための重要な技術について取り上げます。これには入力検証、パラメータクエリ、ストアドプロシージャ、最小権限アクセス制御、ウェブアプリケーションファイアウォールなどが含まれます。

## SQL注入とは何か

SQL注入は、攻撃者がSQLクエリフィールドに専門的なコマンドを挿入することで、バックエンドデータベース操作を操作するコード注入技術です。これらの攻撃は、感度の高いデータを公開し、データを操作または破壊し、攻撃者がデータベースサーバーの完全制御を得る可能性があります。

## SQL注入対策技術の主要機能

### 1. 入力検証とサニタイズ

**説明:** ユーザー入力が処理される前に、データ型、長さ、範囲を確認し、SQLクエリを Manipulate できる特別な文字を削除またはエスケープします。

**例:** Pythonで`re`を使用して正規表現を使用して入力値を検証または`psycopg2`を使用してパラメータクエリを使用します。

```python
import re

def sanitize_input(input_str):
    pattern = re.compile(r"[^a-zA-Z0-9]+")
    return pattern.sub('', input_str)

username = sanitize_input(username)
password = sanitize_input(password)
```

### 2. パラメータクエリ（プレペアドステートメント）

**説明:** SQLステートメントをデータ値のプレースホルダーで予めコンパイルするパラメータクエリを使用します。これにより、ユーザー入力はデータとして扱われるため、実行可能なコードとして扱われる Risk が軽減されます。

**例:** Pythonで`sqlite3`を使用して`sqlite3.Cursor.execute()`とパラメータを使用します:

```python
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", ('user1', 'pass1'))
results = cursor.fetchall()
```

### 3. ストアドプロシージャ

**説明:** データベースで予めコンパイルされたストアドプロシージャを使用して、パラメータで実行します。これにより、SQL注入の Risk が軽減される可能性があります。実行環境を制御し、ユーザーがデータベースに直接アクセスするのを制限します。

**例:** MySQLでストアドプロシージャを作成します:

```sql
DELIMITER //
CREATE PROCEDURE getUser(IN username VARCHAR(50))
BEGIN
    SELECT * FROM users WHERE username = username;
END //
DELIMITER ;
```

### 4. 最小権限アクセス制御

**説明:** アプリケーションが機能するための必要な権限に制限します。これにより、攻撃者がアクセスした場合の Potential 損失が減ります。

**例:** 必要な権限をデータベースユーザに付与します。SELECT, INSERT, UPDATE, DELETEなどの権限があります。

```sql
GRANT SELECT, INSERT ON database.users TO 'user'@'localhost';
```

### 5. ウェブアプリケーションファイアウォール（WAF）

**説明:** WAFを使用して、アプリケーションに到達する前に悪意のあるトラフィックをフィルタリングおよびブロックします。WAFは、HTTPトラフィックを分析してSQL注入攻撃を検出および防止します。

**例:** ApacheのModSecurityまたはAWSのAWS WAFを使用します。

```apache
# ModSecurity設定
<IfModule mod_security2.c>
    SecRuleEngine On
    SecDefaultAction "phase:2,log,deny,status:403,msg:'Potential SQL injection attempt'"
    SecRule REQUEST_URI "/path/to/vulnerable/script.php" "phase:2,t:none,t:lowercase,t:urlDecode,t:htmlEntityDecode,pass,nolog,chain"
    SecRule ARGUMENTS "@rx (union|select|insert|delete|update|drop|count|chr|mid|master|truncate|char|declare|and|or|if|xp|execute|exec|sql)" "id:1000,msg:'Potential SQL injection detected',logdata:'$MATCHED_VAR $MATCHED_VARLINE',$MATCHED_VAR,$MATCHED_VARLINE"
</IfModule>
```

### 6. セキュリティフレームワークとライブラリの使用

**説明:** SQL注入を防ぐために構築されたセキュリティフレームワークとライブラリを使用します。Ruby on Rails、Django（Python）、Spring（Java）などのフレームワークは、SQL注入を防ぐ機能を提供しています。

**例:** DjangoでクエリセットとORMを使用してデータベースとの相互作用を安全に行います:

```python
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

def get_user(username, password):
    return User.objects.filter(username=username, password=password)
```

### 7. コードレビューとセキュリティテスト

**説明:** セキュリティ脆弱性を定期的にレビューし、静的解析、動的解析、ペンetration テスト、脆弱性スキャンなどのセキュリティテストを実施します。

**例:** OWASP ZAP、Veracode、静的コード解析ツールのSonarQubeを使用します。

```python
# OWASP ZAPを使用したシンプルなセキュリティテスト
import zapv2

zap = zapv2.ZAPv2('http://localhost:8080')
zap.urlopen('http://example.com')
zap.ascan.scan('http://example.com')
```

### 8. エラー処理とログ記録

**説明:** 例外を処理し、セキュリティに関連するイベントをログ記録しますが、感度の高い情報を公開しないようにします。

**例:** Pythonでtry-exceptブロックを使用してエラーを処理します:

```python
import logging

logger = logging.getLogger(__name__)

try:
    cursor.execute(query)
except Exception as e:
    logger.error(f"Error executing query: {e}")
```

## 歴史

SQL注入の技術はウェブ開発の初期段階から存在してきました。最初にドキュメンテーションされたSQL注入脆弱性は1995年にありました。それ以来、多数のセキュリティ措置が開発され、磨かれ、上記のものに含まれるものがあります。

## 使用例

- **ウェブ開発:** データベースと互換性のあるあらゆるウェブアプリケーションはSQL注入の可能性があります。
- **データベース管理:** マネージャーは適切な構成とセキュリティ実践を確保してSQL注入を防止する必要があります。
- **セキュリティ監査:** 定期的なセキュリティ評価とペンetration テストにより、SQL注入脆弱性を特定し、軽減できます。

## インストールと基本的な使用法

### Pythonのパラメータクエリ（sqlite3）

**インストール:** PythonでSQLite3はデフォルトで含まれています。

**基本的な使用法:**

```python
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", ('user1', 'pass1'))
results = cursor.fetchall()
```

### MySQLのストアドプロシージャ

**インストール:** MySQLサーバーのインストール。

**基本的な使用法:**

```sql
DELIMITER //
CREATE PROCEDURE getUser(IN username VARCHAR(50))
BEGIN
    SELECT * FROM users WHERE username = username;
END //
DELIMITER ;
```

### ウェブアプリケーションファイアウォール（WAF）の使用

**インストール:** WAFソフトウェアをダウンロードまたはインストールするか、クラウドベースのWAFサービスを使用します。

**基本的な使用法:**

- WAFを設定してSQL注入攻撃を検出してブロックします。
- 新しい脅威に適応するため、WAFルールを定期的に更新します。

これらの対策技術を実装することで、開発者と管理者はSQL注入攻撃の Risk を大幅に軽減し、アプリケーションのセキュリティを確保できます。