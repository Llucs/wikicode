---
title: Projetando APIs REST Limpas em Go
description: Um guia prático para construir APIs REST sustentáveis e testáveis em Go usando padrões estabelecidos e ferramentas da biblioteca padrão.
created: 2026-06-03
tags:
  - guide
  - backend
  - language-go
  - api-design
status: stable
---

# Projetando APIs REST Limpas em Go

A biblioteca padrão e o ecossistema maduro do Go tornam-no uma excelente escolha para construir APIs REST. Este guia aborda os padrões e práticas que produzem serviços sustentáveis e testáveis.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## Estrutura do projeto

Uma API Go bem organizada segue um layout de pacotes consistente:

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

Mantenha os pacotes internos privados. Exporte apenas o que outros projetos precisam consumir do seu código. Use `cmd/` para pontos de entrada da aplicação e `internal/` para pacotes que nunca devem ser importados fora deste projeto.

## Roteamento HTTP com net/http

A biblioteca padrão do Go lida com roteamento manualmente, mas para qualquer coisa além de serviços triviais, use um roteador que suporte correspondência de métodos e parâmetros. O roteador [`chi`](https://github.com/go-chi/chi) é leve, idiomático e amplamente adotado.

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

## Manipulação de requisições

Separe as responsabilidades claramente: handlers recebem requisições HTTP, chamam serviços e formatam respostas. Nunca deixe consultas ao banco de dados vazarem para os handlers.

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

## Codificação e decodificação JSON

O `encoding/json` do Go é seguro por padrão, mas lento. Para serviços de alto throughput, use `github.com/goccy/go-json` ou `github.com/json-iterator/go`. Sempre decodifique para um struct de requisição, nunca para `map[string]interface{}`.

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

## Tratamento de erros

Defina erros específicos de domínio para que os handlers possam mapeá-los para códigos de status HTTP. Nunca exponha erros brutos de banco de dados aos clientes.

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

## Middleware

Use middleware para preocupações transversais: logging, autenticação, limitação de taxa. Encadeie middleware no roteador.

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

## Testando handlers

Teste handlers isoladamente passando um `*httptest.ResponseRecorder` e um `*http.Request`. Use testes orientados por tabela para múltiplos cenários.

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

## Tópicos relacionados

- [Padrão Repository em Go](https://christiancurteanu.com/5-api-design-patterns-in-go-that-solve-your-biggest-problems-2025) — separe o acesso a dados da lógica de negócios para testabilidade.
- [Estratégias de teste de API Go](https://blog.stackademic.com/golang-use-restful-api-like-a-pro-best-practices-for-restful-apis-in-golang-39d808fbbdb6) — testes de integração e contrato para serviços REST.
- A [documentação do roteador Chi](https://github.com/go-chi/chi) cobre roteamento, middleware e propagação de contexto em profundidade.