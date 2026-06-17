---
title: "GoでのREST API — 完全なプロジェクト"
description: Gin、SQLite、JWT、クリーンアーキテクチャパターンを使用したGoによる完全なREST API。
created: 2026-06-14
tags:
  - project
  - go
  - rest-api
  - backend
status: draft
---

# GoでのREST API

## 概要

Goで構築された本番環境向けREST API。JWT認証、SQLiteストレージ、レイヤードアーキテクチャを特徴としています。

## スタック

- **言語:** Go 1.22+
- **ルーター:** Gin
- **データベース:** SQLite (via modernc.org/sqlite)
- **認証:** JWT (golang-jwt/jwt/v5)
- **テスト:** testing + httptest

## エンドポイント

| メソッド | ルート             | 説明               |
|---------|-------------------|-------------------|
| POST    | /api/v1/register  | ユーザー登録       |
| POST    | /api/v1/login     | ログイン           |
| GET     | /api/v1/profile   | プロフィール取得（認証必須） |
| PUT     | /api/v1/profile   | プロフィール更新   |

## コアコード

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

## セットアップ

```bash
git clone <repo> && cd projects/create-a-real-world-rest-api-project-in-go
go mod init myapi
go mod tidy
go run cmd/server/main.go
```

## テスト

```bash
go test ./...
```