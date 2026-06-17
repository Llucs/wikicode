---
title: REST API in Go — Vollständiges Projekt
description: Eine vollständige REST API in Go mit Gin, SQLite, JWT und sauberen Architekturmustern.
created: 2026-06-14
tags:
  - project
  - go
  - rest-api
  - backend
status: draft
---

# REST API in Go

## Übersicht

Eine produktionsorientierte REST API, erstellt mit Go, mit JWT-Authentifizierung, SQLite-Speicherung und Schichtenarchitektur.

## Technologie-Stack

- **Sprache:** Go 1.22+
- **Router:** Gin
- **Datenbank:** SQLite (via modernc.org/sqlite)
- **Authentifizierung:** JWT (golang-jwt/jwt/v5)
- **Testen:** testing + httptest

## Endpunkte

| Methode | Route             | Beschreibung          |
|---------|-------------------|-----------------------|
| POST    | /api/v1/register  | Benutzer registrieren |
| POST    | /api/v1/login     | Anmelden              |
| GET     | /api/v1/profile   | Profil abrufen (Auth) |
| PUT     | /api/v1/profile   | Profil aktualisieren  |

## Kerncode

### cmd/server/main.go

```go
package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	"myapi/internal/handler"
	"myapi/internal/middleware"
	"myapi/internal/repository"
	"myapi/internal/service"
)

func main() {
	db := repository.NewSQLite("data.db")
	if err := db.Migrate(); err != nil {
		log.Fatal(err)
	}

	authSvc := service.NewAuthService(db)
	userSvc := service.NewUserService(db)

	r := gin.Default()
	r.Use(middleware.CORS())

	api := r.Group("/api/v1")
	{
		api.POST("/register", handler.Register(authSvc))
		api.POST("/login", handler.Login(authSvc))

		auth := api.Group("")
		auth.Use(middleware.AuthJWT())
		{
			auth.GET("/profile", handler.GetProfile(userSvc))
			auth.PUT("/profile", handler.UpdateProfile(userSvc))
		}
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Server running on :%s", port)
	r.Run(":" + port)
}
```

### internal/handler/auth.go

```go
package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"myapi/internal/service"
)

func Register(svc *service.AuthService) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req struct {
			Email    string `json:"email" binding:"required,email"`
			Password string `json:"password" binding:"required,min=6"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		user, err := svc.Register(req.Email, req.Password)
		if err != nil {
			c.JSON(http.StatusConflict, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, user)
	}
}

func Login(svc *service.AuthService) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req struct {
			Email    string `json:"email" binding:"required"`
			Password string `json:"password" binding:"required"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		token, err := svc.Login(req.Email, req.Password)
		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"token": token})
	}
}
```

### internal/middleware/auth.go

```go
package middleware

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = []byte("change-me-in-production")

func AuthJWT() gin.HandlerFunc {
	return func(c *gin.Context) {
		auth := c.GetHeader("Authorization")
		if !strings.HasPrefix(auth, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing token"})
			return
		}
		tokenStr := strings.TrimPrefix(auth, "Bearer ")
		token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (interface{}, error) {
			return jwtSecret, nil
		})
		if err != nil || !token.Valid {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
			return
		}
		claims := token.Claims.(jwt.MapClaims)
		c.Set("user_id", claims["sub"])
		c.Next()
	}
}
```

## Einrichtung

```bash
git clone <repo> && cd projects/create-a-real-world-rest-api-project-in-go
go mod init myapi
go mod tidy
go run cmd/server/main.go
```

## Tests

```bash
go test ./...
```