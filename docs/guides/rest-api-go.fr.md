---
title: Conception d'APIs REST propres en Go
description: Un guide pratique pour construire des APIs REST maintenables et testables en Go en utilisant des modèles éprouvés et les outils de la bibliothèque standard.
created: 2026-06-03
tags:
  - guide
  - backend
  - language-go
  - api-design
status: stable
---

# Conception d'APIs REST propres en Go

La bibliothèque standard de Go et son écosystème mature en font un excellent choix pour construire des APIs REST. Ce guide couvre les modèles et les pratiques qui produisent des services maintenables et testables.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé: 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour: auto (git)</span>
</div>

## Structure du projet

Un projet Go bien organisé suit une disposition de packages cohérente :

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

Gardez les packages internes privés. Exportez uniquement ce dont les autres projets ont besoin pour consommer votre code. Utilisez `cmd/` pour les points d'entrée de l'application et `internal/` pour les packages qui ne doivent jamais être importés en dehors de ce projet.

## Routage HTTP avec net/http

La bibliothèque standard de Go gère le routage manuellement, mais pour tout ce qui dépasse les services triviaux, utilisez un routeur qui supporte la correspondance des méthodes et des paramètres. Le routeur [`chi`](https://github.com/go-chi/chi) est léger, idiomatique et largement adopté.

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

## Gestion des requêtes

Séparez clairement les préoccupations : les handlers reçoivent les requêtes HTTP, appellent les services et formatent les réponses. Ne laissez jamais les requêtes de base de données s'infiltrer dans les handlers.

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

## Encodage et décodage JSON

L'`encoding/json` de Go est sûr par défaut mais lent. Pour les services à haut débit, utilisez `github.com/goccy/go-json` ou `github.com/json-iterator/go`. Décodez toujours dans une structure de requête, jamais dans `map[string]interface{}`.

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

## Gestion des erreurs

Définissez des erreurs spécifiques au domaine afin que les handlers puissent les mapper aux codes d'état HTTP. N'exposez jamais les erreurs brutes de la base de données aux clients.

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

Utilisez le middleware pour les préoccupations transversales : journalisation, authentification, limitation de débit. Enchaînez le middleware dans le routeur.

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

## Test des handlers

Testez les handlers en isolation en passant un `*httptest.ResponseRecorder` et une `*http.Request`. Utilisez des tests pilotés par table pour plusieurs scénarios.

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

## Sujets voisins

- [Le pattern Repository en Go](https://christiancurteanu.com/5-api-design-patterns-in-go-that-solve-your-biggest-problems-2025) — séparez l'accès aux données de la logique métier pour la testabilité.
- [Stratégies de test d'API Go](https://blog.stackademic.com/golang-use-restful-api-like-a-pro-best-practices-for-restful-apis-in-golang-39d808fbbdb6) — tests d'intégration et de contrat pour les services REST.
- La [documentation du routeur Chi](https://github.com/go-chi/chi) couvre en détail le routage, le middleware et la propagation du contexte.