---
title: Go 语言 REST API — 完整项目
description: 一个使用 Gin、SQLite、JWT 和整洁架构模式的完整 Go 语言 REST API。
created: 2026-06-14
tags:
  - project
  - go
  - rest-api
  - backend
status: draft
---

# Go 语言 REST API

## 概述

一个面向生产的 REST API，使用 Go 构建，具备 JWT 认证、SQLite 存储和分层架构。

## 技术栈

- **语言：** Go 1.22+
- **路由：** Gin
- **数据库：** SQLite（通过 modernc.org/sqlite）
- **认证：** JWT（golang-jwt/jwt/v5）
- **测试：** testing + httptest

## 接口端点

| 方法 | 路由             | 描述          |
|------|------------------|---------------|
| POST | /api/v1/register | 注册用户      |
| POST | /api/v1/login    | 登录          |
| GET  | /api/v1/profile  | 获取个人资料（需认证） |
| PUT  | /api/v1/profile  | 更新个人资料  |

## 核心代码

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

## 设置

```bash
git clone <repo> && cd projects/create-a-real-world-rest-api-project-in-go
go mod init myapi
go mod tidy
go run cmd/server/main.go
```

## 测试

```bash
go test ./...
```