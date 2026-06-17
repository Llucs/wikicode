---
title: GoにおけるクリーンなREST APIの設計
description: Goで保守可能かつテスト可能なREST APIを構築するための実践的ガイド。確立されたパターンと標準ライブラリのツールを使用します。
created: 2026-06-03
tags:
  - guide
  - backend
  - language-go
  - api-design
status: stable
---

# GoにおけるクリーンなREST APIの設計

Goの標準ライブラリと成熟したエコシステムは、REST APIを構築するための優れた選択肢です。このガイドでは、保守可能でテスト可能なサービスを生み出すパターンとプラクティスを説明します。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">作成日: 2026-06-03</span>
<span class="wikicode-meta-updated">最終更新: auto (git)</span>
</div>

## プロジェクト構造

よく構成されたGo APIは、一貫したパッケージレイアウトに従います。

```
myapi/
├── cmd/
│   └── server/
│       └── main.go          # Application entrypoint
├── internal/
│   ├── handler/             # HTTP handlers
│   ├── middleware/          # Middleware functions
│   ├── model/                # Domain models
│   ├── repository/          # Data access layer
│   └── service/             # Business logic
├── pkg/                     # Shared packages (optional)
├── go.mod
└── go.sum
```

internal パッケージはプライベートに保ってください。他のプロジェクトがあなたのコードを利用するために必要なものだけをエクスポートします。`cmd/` をアプリケーションのエントリポイントに、`internal/` をこのプロジェクトの外部からインポートされるべきでないパッケージに使用してください。

## net/http による HTTP ルーティング

Goの標準ライブラリは手動でルーティングを処理しますが、簡単なサービスを超える場合には、メソッドとパラメータのマッチングをサポートするルーターを使用してください。`chi` ルーターは軽量でGoらしく、広く採用されています。

```go
package main

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func main() {
	r := chi.NewRouter()

	// Global middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)

	// Routes
	r.Route("/api/v1", func(r chi.Router) {
		r.Get("/users", listUsers)
		r.Post("/users", createUser)
		r.Get("/users/{id}", getUser)
		r.Put("/users/{id}", updateUser)
		r.Delete("/users/{id}", deleteUser)
	})

	http.ListenAndServe(":8080", r)
}
```

## リクエスト処理

関心を明確に分離します。ハンドラはHTTPリクエストを受け取り、サービスを呼び出し、レスポンスをフォーマットします。データベースクエリがハンドラに漏れ出ることがないようにしてください。

```go
// handler/user.go
package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"myapi/internal/service"
)

type UserHandler struct {
	svc service.UserService
}

func NewUserHandler(svc service.UserService) *UserHandler {
	return &UserHandler{svc: svc}
}

// GET /users
func (h *UserHandler) listUsers(w http.ResponseWriter, r *http.Request) {
	users, err := h.svc.List(r.Context())
	if err != nil {
		respondError(w, r, err)
		return
	}
	respondJSON(w, http.StatusOK, users)
}

// GET /users/{id}
func (h *UserHandler) getUser(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	if err != nil {
		respondError(w, r, errInvalidID)
		return
	}

	user, err := h.svc.Get(r.Context(), id)
	if err != nil {
		respondError(w, r, err)
		return
	}
	respondJSON(w, http.StatusOK, user)
}
```

## JSON エンコードとデコード

Goの `encoding/json` はデフォルトで安全ですが遅いです。高スループットのサービスでは、`github.com/goccy/go-json` または `github.com/json-iterator/go` を使用してください。常にリクエスト構造体にデコードし、`map[string]interface{}` にデコードしないでください。

```go
type CreateUserRequest struct {
	Email    string `json:"email"`
	Name     string `json:"name"`
	Password string `json:"password"`
}

func (h *UserHandler) createUser(w http.ResponseWriter, r *http.Request) {
	var req CreateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, r, errBadRequest(err))
		return
	}
	defer r.Body.Close()

	if req.Email == "" || req.Password == "" {
		respondError(w, r, errMissingFields)
		return
	}

	user, err := h.svc.Create(r.Context(), req.Email, req.Name, req.Password)
	if err != nil {
		respondError(w, r, err)
		return
	}
	respondJSON(w, http.StatusCreated, user)
}
```

## エラーハンドリング

ドメイン固有のエラーを定義して、ハンドラがそれらをHTTPステータスコードにマッピングできるようにします。生のデータベースエラーをクライアントに公開しないでください。

```go
// model/errors.go
package model

import (
	"errors"
	"fmt"
)

var (
	ErrNotFound     = errors.New("not found")
	ErrInvalidInput = errors.New("invalid input")
	ErrDuplicate    = errors.New("duplicate")
)

// APIError carries an HTTP status code alongside the error.
type APIError struct {
	Status  int
	Message string
	Cause   error
}

func (e *APIError) Error() string {
	if e.Cause != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Cause)
	}
	return e.Message
}

func (e *APIError) Unwrap() error {
	return e.Cause
}
```

```go
// handler/response.go
package handler

import (
	"encoding/json"
	"net/http"
)

// ErrorResponse maps to the JSON body returned on errors.
type ErrorResponse struct {
	Error   string `json:"error"`
	Code    int    `json:"code,omitempty"`
	Details string `json:"details,omitempty"`
}

func respondJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(v)
}

func respondError(w http.ResponseWriter, r *http.Request, err error) {
	var apiErr *model.APIError
	if errors.As(err, &apiErr) {
		respondJSON(w, apiErr.Status, ErrorResponse{
			Error: apiErr.Message,
			Code:  apiErr.Status,
		})
		return
	}

	// Unknown error — log and return 500
	log.Printf("internal error: %v", err)
	respondJSON(w, http.StatusInternalServerError, ErrorResponse{
		Error: "internal server error",
		Code:  http.StatusInternalServerError,
	})
}
```

## ミドルウェア

ミドルウェアを横断的関心事（ログ記録、認証、レート制限）に使用します。ルーター内でミドルウェアをチェーンします。

```go
// middleware/logging.go
package middleware

import (
	"log"
	"net/http"
	"time"
)

func Logger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rw := &responseWriter{ResponseWriter: w, status: http.StatusOK}
		next.ServeHTTP(rw, r)
		log.Printf("%s %s %d %s",
			r.Method, r.URL.Path, rw.status, time.Since(start))
	})
}

type responseWriter struct {
	http.ResponseWriter
	status int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.status = code
	rw.ResponseWriter.WriteHeader(code)
}
```

## ハンドラのテスト

ハンドラを隔離してテストするには、`*httptest.ResponseRecorder` と `*http.Request` を渡します。複数のシナリオにはテーブル駆動テストを使用します。

```go
// handler/user_test.go
package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"myapi/internal/model"
)

func TestListUsers(t *testing.T) {
	svc := &mockUserService{users: []model.User{
		{ID: 1, Email: "alice@example.com", Name: "Alice"},
		{ID: 2, Email: "bob@example.com", Name: "Bob"},
	}}
	h := NewUserHandler(svc)

	req := httptest.NewRequest(http.MethodGet, "/users", nil)
	w := httptest.NewRecorder()
	h.listUsers(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", w.Code)
	}

	var users []model.User
	if err := json.NewDecoder(w.Body).Decode(&users); err != nil {
		t.Fatal(err)
	}
	if len(users) != 2 {
		t.Fatalf("expected 2 users, got %d", len(users))
	}
}
```

## 関連トピック

- [Goにおけるリポジトリパターン](https://christiancurteanu.com/5-api-design-patterns-in-go-that-solve-your-biggest-problems-2025) — テスト容易性のためにデータアクセスをビジネスロジックから分離します。
- [Go API テスト戦略](https://blog.stackademic.com/golang-use-restful-api-like-a-pro-best-practices-for-restful-apis-in-golang-39d808fbbdb6) — RESTサービスの統合テストとコントラクトテスト。
- [Chi ルーターのドキュメント](https://github.com/go-chi/chi) では、ルーティング、ミドルウェア、コンテキストの伝播について詳しく説明されています。