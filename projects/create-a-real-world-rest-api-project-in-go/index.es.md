---
title: API REST en Go — Proyecto Completo
description: Una API REST completa en Go usando Gin, SQLite, JWT y patrones de arquitectura limpia.
created: 2026-06-14
tags:
  - project
  - go
  - rest-api
  - backend
status: draft
---

# API REST en Go

## Resumen

Una API REST orientada a la producción construida con Go, con autenticación JWT, almacenamiento SQLite y arquitectura en capas.

## Stack

- **Lenguaje:** Go 1.22+
- **Router:** Gin
- **Base de datos:** SQLite (via modernc.org/sqlite)
- **Autenticación:** JWT (golang-jwt/jwt/v5)
- **Pruebas:** testing + httptest

## Endpoints

| Método | Ruta             | Descripción       |
|--------|------------------|-------------------|
| POST   | /api/v1/register | Registrar usuario |
| POST   | /api/v1/login    | Iniciar sesión    |
| GET    | /api/v1/profile  | Obtener perfil (autenticado) |
| PUT    | /api/v1/profile  | Actualizar perfil |

## Código principal

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

## Configuración

```bash
git clone <repo> && cd projects/create-a-real-world-rest-api-project-in-go
go mod init myapi
go mod tidy
go run cmd/server/main.go
```

## Pruebas

```bash
go test ./...
```