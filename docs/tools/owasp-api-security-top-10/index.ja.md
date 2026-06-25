---
title: OWASP API Security Top 10
description: OWASP API Security Top Ten (2023)を網羅した包括的な開発者向けWikiです。深掘り解説、テスト戦略、CI/CD統合を含みます。
created: 2026-06-25
tags:
  - owasp
  - api-security
  - top-10
  - bola
  - bopla
  - secure-coding
  - devsecops
  - bug-bounty
status: draft
---

# OWASP API Security Top 10

**OWASP API Security Top 10** は、Open Web Application Security Project (OWASP) が公開する業界標準の認識文書であり、2023年に更新され、現代のREST、GraphQL、gRPC、SOAP APIに固有のセキュリティリスクを反映しています。一般的なOWASP Web Top 10（XSS、SQLi、CSRFなどをカバー）とは異なり、このリストはAPI駆動型アプリケーションを悩ませるアーキテクチャ上の問題や論理上の欠陥に**のみ**焦点を当てています。

2026年現在、APIに関連する障害は依然としてデータ侵害の主要なベクトルであり、主要企業（Twitter、T-Mobile、Optus）でのインシデントは、このフレームワークに文書化されたいくつかの防止可能なミスに起因しています。

---

## APIセキュリティリスク トップ10（2023年）

| 順位 | 名称 | 略語 | 問題の核心 |
|------|------|---------|--------------|
| API1 | Broken Object Level Authorization | BOLA | 適切なACLチェックなしに他のユーザーに属するオブジェクトにアクセスする |
| API2 | Broken Authentication | — | 脆弱な資格情報管理、トークン漏洩、セッションフィクセーション |
| API3 | Broken Object Property Level Authorization | BOPLA | 機密フィールドのマスアサインメント／過剰送信 (over-posting) |
| API4 | Unrestricted Resource Consumption | — | レート制限、ページネーション上限、ペイロードサイズの制限がない |
| API5 | Broken Function Level Authorization | BFLA | 通常ユーザーとして高権限の管理エンドポイントを呼び出す |
| API6 | Unrestricted Access to Sensitive Business Flows | — | ボットによる有効なAPIワークフローの悪用（スカルピング、スクレイピング） |
| API7 | Server Side Request Forgery | SSRF | APIがユーザー制御のURLをフェッチし、内部サービスを探索可能 |
| API8 | Security Misconfiguration | — | デフォルト認証情報、詳細なエラー出力、CORSの欠如、未パッチのシステム |
| API9 | Improper Inventory Management | — | ゾンビ/非推奨APIバージョン、忘れられたデバッグエンドポイント、シャドウAPI |
| API10 | Unsafe Consumption of APIs | — | サードパーティAPIの応答を盲目的に信頼する（サプライチェーンリスク） |

### 2019年からの主な変更点

2023年版では、一般的なWeb脅威（XSS、SQLiなど。現在は標準のTop 10でカバー）を削除し、**BOPLA**、**Unrestricted Business Flows**、**SSRF**、**Improper Inventory Management**、**Unsafe Consumption**の5つのまったく新しいカテゴリを導入しました。

また、**「Lather, Rinse, Repeat」**（泡立てる、すすぐ、繰り返す）方法論を正式化しました。これは、発見（Discovery）→ 検証（Validation）→ 修正（Remediation）の継続的なサイクルです。

---

## 導入方法論

これは*フレームワーク*（ソフトウェアパッケージではありません）であるため、「インストール」とは、考え方とテストフローを開発ライフサイクルに統合することを意味します。

### フェーズ1: 発見とインベントリ（API9に対応）

すべてのエンドポイント、そのデータ感度、認証メカニズム、バージョンをマッピングします。これは最も見落とされがちなステップです。

```bash
# 一般的なAPIパスの簡単な発見スキャン
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "Endpoint ${endpoint} returned ${status}"
done
```

ツール: Postman, Swagger Inspector, Burp Suite, カスタムクローラ。

### フェーズ2: 自動スキャン

API仕様に対して動的スキャナを実行します。

```bash
# OWASP ZAP APIスキャン
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**自動で実行すべき主要なチェック:**
- **BOLA:** 一括リクエストでオブジェクトIDを入れ替える。
- **BFLA:** 低権限トークンで管理エンドポイントに対してDELETE/PUTを試みる。
- **SSRF:** URLパラメータに `http://169.254.169.254/metadata/instance` を注入する。
- **Misconfiguration:** `Access-Control-Allow-Origin: *` の有無や詳細なエラー応答をチェックする。

### フェーズ3: 手動による詳細調査（ペネトレーションテストモード）

Top 10をチェックリストとして使用します。

#### API1: 壊れたオブジェクトレベル認可（BOLA）

```bash
# URL内のIDを変更して別のユーザーのデータにアクセスを試みる
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# レスポンスにユーザー123のデータが含まれる場合、BOLA脆弱性が存在します。
```

#### API3: 壊れたオブジェクトプロパティレベル認可（BOPLA）

```bash
# マスアサインメント: PATCH に "role":"admin" や "salary":100000 を追加してみる
curl -X PATCH https://api.example.com/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","salary":999999}'
```

#### API6: 制限のないビジネスフロー

```python
import requests
# 投票 / クーポン / チェックアウトフローを悪用するボットをシミュレート
url = "https://ticketing.example.com/api/v2/checkout"
payload = {"event_id": 1, "quantity": 1}
session = requests.Session()
session.headers.update({"Authorization": "Bearer valid_token"})

for i in range(100):
    r = session.post(url, json=payload)
    print(f"Attempt {i}: {r.status_code} - {r.text[:100]}")
    # 100回すべて成功し、レート制限がない場合はAPI6が存在します。
```

### フェーズ4: CI/CD統合

チェックをパイプラインに組み込みます。典型的なセキュアパイプラインのステージ例:

```yaml
# .gitlab-ci.yml (GitLab CI) または同等のGitHub Actions
api-security:
  stage: test
  script:
    # BOPLAパターンの静的解析
    - semgrep --config=auto .
    # ZAPによる動的スキャン
    - docker run -v $(pwd):/zap/wrk/ zaproxy/zap-stable \
        zap-api-scan.py -t http://staging/api/openapi.json -f openapi
    # レート制限 / ビジネスフロー悪用テスト（k6）
    - k6 run tests/abuse.js
  only:
    - branches
```

#### 例：BOPLA（Djangoでのマスアサインメント）に対するSemgrepルール

```yaml
rules:
  - id: mass-assignment-django
    patterns:
      - pattern-either:
          - pattern: Model.objects.update(...)  # フィールドをフィルタリングしない場合、危険
          - pattern: serializer.save(...)
    message: >
      マスアサインメントの脆弱性の可能性 (API3 / BOPLA)。
      シリアライザで `fields` または `read_only_fields` を使用して、許可されるフィールドを明示的に定義してください。
    severity: WARNING
    languages:
      - python
```

#### 例：レート制限ミドルウェア（Go）

```go
import (
    "golang.org/x/time/rate"
    "net/http"
)

var limiter = rate.NewLimiter(rate.Limit(100), 200) // 100リクエスト/秒、バースト200

func rateLimitMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !limiter.Allow() {
            http.Error(w, `{"error":"rate_limit_exceeded"}`, http.StatusTooManyRequests)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

## 「Lather, Rinse, Repeat」方法論

2023年版で特に強調されているこの概念は、APIセキュリティは**1回限りのペネトレーションテストではなく**、継続的なサイクルであることを強調しています:

1. **Lather:** APIサーフェス全体（シャドウAPIを含む）を発見する。
2. **Rinse:** 自動テストと手動テストを通じて発見事項を検証する。
3. **Repeat:** 新しいエンドポイントやバージョンがデプロイされるたびに再スキャンする。

これは**API9（不適切なインベントリ管理）**に直接対抗し、セキュリティ態勢がコードベースとともに進化することを保証します。

## 他の標準との関係

- **PCI DSS 4.0:** カード会員データ環境に対して、堅牢なAPIセキュリティコントロール（BOLA/BFLAテストを含む）を要求します。
- **SOC 2:** Top 10は、可用性およびセキュリティ基準のための具体的なコントロールフレームワークを提供します。
- **ISO 27001:** 論理アクセスと運用セキュリティに関する附属書Aのコントロールの構造化に役立ちます。
- **OWASP Web Top 10:** 補完的です。常に両方のリストを確認してください。Web Top 10はインジェクションと暗号化をカバーし、API Top 10はロジックとビジネス欠陥をカバーします。

## API Security Top 10を使用すべきでない場合

- これは**認識文書**であり、厳格なコンプライアンス基準ではありません。出発点として扱い、網羅的な監査チェックリストとしては使用しないでください。
- 暗号化、ログ記録、物理的セキュリティについては詳細にカバーしていません（それらについてはASVSまたはMASVSを参照してください）。
- 特定のアーキテクチャに合わせた脅威モデルの代わりには*なりません*。

## 主要なポイント

| リスク | 主な緩和策 | テスト例 |
|------|--------------------|--------------|
| BOLA | すべてのオブジェクトアクセスに対して厳格な所有権チェックを要求する。 | GETリクエストでIDを入れ替える。 |
| BOPLA | DTO/ViewModelを使用し、ユーザーオブジェクトをORMに直接渡さない。 | `role` や `admin` フィールドを注入する。 |
| SSRF | プライベートIP範囲を拒否リストにし、送信先を許可リストで管理する。 | メタデータエンドポイント（`169.254.169.254`）をフェッチする。 |
| Business Flows | 機密性の高いアクションに対するレート制限 + CAPTCHA。 | チェックアウトを100回自動化する。 |
| Inventory | CIパイプラインで生きたAPIカタログを維持する。 | `v1/`、`swagger.json`、`/debug` をクロールする。 |

## 参考文献

- OWASP API Security Project 公式: [https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Top 10 Web (2021): [https://owasp.org/Top10/](https://owasp.org/Top10/)
- OWASP ZAP API Scanning: [https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- APIセキュリティ向けSemgrepルール: [https://semgrep.dev](https://semgrep.dev)

---

*ステータス: draft. 最終更新: 2026-06-25.*