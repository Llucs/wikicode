---
title: Diseñando APIs REST limpias en Go
description: Una guía práctica para construir APIs REST mantenibles y testeables en Go utilizando patrones establecidos y herramientas de la biblioteca estándar.
created: 2026-06-03
tags:
  - guide
  - backend
  - language-go
  - api-design
status: stable
---

# Diseñando APIs REST limpias en Go

La biblioteca estándar de Go y su ecosistema maduro lo convierten en una excelente opción para construir APIs REST. Esta guía cubre los patrones y prácticas que producen servicios mantenibles y testeables.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## Estructura del proyecto

Una API de Go bien organizada sigue una disposición de paquetes consistente:

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

Mantén los paquetes internal privados. Solo exporta lo que otros proyectos necesiten consumir de tu código. Usa `cmd/` para puntos de entrada de la aplicación e `internal/` para paquetes que nunca deberían ser importados fuera de este proyecto.

## Enrutamiento HTTP con net/http

La biblioteca estándar de Go maneja el enrutamiento manualmente, pero para cualquier cosa más allá de servicios triviales, usa un enrutador que soporte coincidencia de métodos y parámetros. El enrutador [`chi`](https://github.com/go-chi/chi) es ligero, idiomático y ampliamente adoptado.

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

## Manejo de solicitudes

Separa las preocupaciones claramente: los handlers reciben solicitudes HTTP, llaman a servicios y formatean respuestas. Nunca permitas que las consultas a la base de datos se filtren en los handlers.

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

## Codificación y decodificación JSON

El `encoding/json` de Go es seguro por defecto pero lento. Para servicios de alto rendimiento, usa `github.com/goccy/go-json` o `github.com/json-iterator/go`. Siempre decodifica en una estructura de solicitud, nunca en `map[string]interface{}`.

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

## Manejo de errores

Define errores específicos del dominio para que los handlers puedan mapearlos a códigos de estado HTTP. Nunca expongas errores crudos de base de datos a los clientes.

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

Usa middleware para preocupaciones transversales: logging, autenticación, limitación de tasa. Encadena middleware en el enrutador.

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

## Pruebas de handlers

Prueba los handlers de forma aislada pasando un `*httptest.ResponseRecorder` y un `*http.Request`. Usa pruebas basadas en tablas para múltiples escenarios.

```go
// handler/user_test.go
package handler

import (
	"encoding/json"
	"net/http"
	"net/http/httpli
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

## Temas relacionados

- [Patrón Repository en Go](https://christiancurteanu.com/5-api-design-patterns-in-go-that-solve-your-biggest-problems-2025) — separa el acceso a datos de la lógica de negocio para mejorar la testabilidad.
- [Estrategias de prueba de API en Go](https://blog.stackademic.com/golang-use-restful-api-like-a-pro-best-practices-for-restful-apis-in-golang-39d808fbbdb6) — pruebas de integración y de contrato para servicios REST.
- La [documentación del enrutador Chi](https://github.com/go-chi/chi) cubre enrutamiento, middleware y propagación de contexto en profundidad.