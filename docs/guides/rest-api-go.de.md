---
title: Entwicklung sauberer REST-APIs in Go
description: Ein praktischer Leitfaden zum Erstellen wartbarer und testbarer REST-APIs in Go unter Verwendung etablierter Muster und der Standardbibliothek.
created: 2026-06-03
tags:
  - guide
  - backend
  - language-go
  - api-design
status: stable
---

# Entwicklung sauberer REST-APIs in Go

Die Go-Standardbibliothek und das ausgereifte Ökosystem machen Go zu einer hervorragenden Wahl für den Bau von REST-APIs. Dieser Leitfaden behandelt die Muster und Praktiken, die wartbare, testbare Dienste hervorbringen.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: automatisch (git)</span>
</div>

## Projektstruktur

Eine gut organisierte Go-API folgt einer konsistenten Paketstruktur:

```
myapi/
├── cmd/
│   └── server/
│       └── main.go          # Anwendungseinstiegspunkt
├── internal/
│   ├── handler/             # HTTP-Handler
│   ├── middleware/          # Middleware-Funktionen
│   ├── model/                # Domain-Modelle
│   ├── repository/          # Datenzugriffsschicht
│   └── service/             # Geschäftslogik
├── pkg/                     # Gemeinsame Pakete (optional)
├── go.mod
└── go.sum
```

Behalten Sie interne Pakete privat. Exportieren Sie nur, was andere Projekte benötigen, um Ihren Code zu verwenden. Verwenden Sie `cmd/` für Anwendungseinstiegspunkte und `internal/` für Pakete, die niemals außerhalb dieses Projekts importiert werden sollten.

## HTTP-Routing mit net/http

Die Go-Standardbibliothek behandelt Routing manuell, aber für alles, was über triviale Dienste hinausgeht, verwenden Sie einen Router, der Methoden- und Parametermatching unterstützt. Der [`chi`](https://github.com/go-chi/chi) Router ist leichtgewichtig, idiomatisch und weit verbreitet.

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

## Anfrageverarbeitung

Trennen Sie die Belange klar: Handler empfangen HTTP-Anfragen, rufen Dienste auf und formatieren Antworten. Lassen Sie niemals Datenbankabfragen in Handler durchsickern.

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

## JSON-Kodierung und -Dekodierung

Das `encoding/json` von Go ist standardmäßig sicher, aber langsam. Verwenden Sie für Dienste mit hohem Durchsatz `github.com/goccy/go-json` oder `github.com/json-iterator/go`. Dekodieren Sie immer in eine Anfrage-Struktur, niemals in `map[string]interface{}`.

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

## Fehlerbehandlung

Definieren Sie domainspezifische Fehler, damit Handler sie HTTP-Statuscodes zuordnen können. Legen Sie niemals rohe Datenbankfehler gegenüber Clients offen.

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

Verwenden Sie Middleware für querschnittliche Belange: Protokollierung, Authentifizierung, Ratenbegrenzung. Verketten Sie Middleware im Router.

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

## Testen von Handlern

Testen Sie Handler isoliert, indem Sie einen `*httptest.ResponseRecorder` und einen `*http.Request` übergeben. Verwenden Sie tabellengetriebene Tests für mehrere Szenarien.

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

## Verwandte Themen

- [Repository-Pattern in Go](https://christiancurteanu.com/5-api-design-patterns-in-go-that-solve-your-biggest-problems-2025) — trennen Sie den Datenzugriff von der Geschäftslogik für Testbarkeit.
- [Go-API-Teststrategien](https://blog.stackademic.com/golang-use-restful-api-like-a-pro-best-practices-for-restful-apis-in-golang-39d808fbbdb6) — Integrations- und Vertragstests für REST-Dienste.
- Die [Chi-Router-Dokumentation](https://github.com/go-chi/chi) behandelt Routing, Middleware und Context-Propagation eingehend.