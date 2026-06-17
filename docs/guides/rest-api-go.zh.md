---
title: 在 Go 中设计整洁的 REST API
description: 使用既定模式和标准库工具在 Go 中构建可维护、可测试的 REST API 的实用指南。
created: 2026-06-03
tags:
  - guide
  - backend
  - language-go
  - api-design
status: stable
---

# 在 Go 中设计整洁的 REST API

Go 的标准库和成熟的生态系统使其成为构建 REST API 的绝佳选择。本指南涵盖了产生可维护、可测试服务的模式和实践。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建于: 2026-06-03</span>
<span class="wikicode-meta-updated">最后更新: 自动 (git)</span>
</div>

## 项目结构

一个组织良好的 Go API 遵循一致的包布局：

```
myapi/
├── cmd/
│   └── server/
│       └── main.go          # 应用程序入口
├── internal/
│   ├── handler/             # HTTP 处理器
│   ├── middleware/          # 中间件函数
│   ├── model/                # 领域模型
│   ├── repository/          # 数据访问层
│   └── service/             # 业务逻辑
├── pkg/                     # 共享包（可选）
├── go.mod
└── go.sum
```

保持内部包私有。只导出其他项目消费你的代码所需的内容。使用 `cmd/` 作为应用程序入口点，使用 `internal/` 作为绝不应在此项目外部导入的包。

## 使用 net/http 进行 HTTP 路由

Go 的标准库手动处理路由，但对于任何超出简单服务的场景，请使用支持方法和参数匹配的路由器。[`chi`](https://github.com/go-chi/chi) 路由轻量、地道且被广泛采用。

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

	// 全局中间件
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)

	// 路由
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

## 请求处理

清晰分离关注点：处理器接收 HTTP 请求，调用服务并格式化响应。绝不让数据库查询泄露到处理器中。

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

## JSON 编码与解码

Go 的 `encoding/json` 默认安全但速度慢。对于高吞吐量服务，使用 `github.com/goccy/go-json` 或 `github.com/json-iterator/go`。始终解码到请求结构体中，绝不解码到 `map[string]interface{}`。

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

## 错误处理

定义领域特定错误，以便处理器可以将它们映射到 HTTP 状态码。绝不要向客户端暴露原始数据库错误。

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

## 中间件

使用中间件处理横切关注点：日志记录、身份验证、速率限制。在路由器中链式使用中间件。

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

## 测试处理器

通过传递 `*httptest.ResponseRecorder` 和 `*http.Request` 来隔离测试处理器。对多种场景使用表驱动测试。

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

## 相关主题

- [Go 中的仓储模式](https://christiancurteanu.com/5-api-design-patterns-in-go-that-solve-your-biggest-problems-2025) — 分离数据访问与业务逻辑以实现可测试性。
- [Go API 测试策略](https://blog.stackademic.com/golang-use-restful-api-like-a-pro-best-practices-for-restful-apis-in-golang-39d808fbbdb6) — REST 服务的集成测试和契约测试。
- [Chi 路由文档](https://github.com/go-chi/chi) 深入介绍了路由、中间件和上下文传播。