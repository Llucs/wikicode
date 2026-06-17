---
title: cURL — 数据传输工具
description: cURL 是一款使用网络协议进行数据传输的命令行工具。
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
ecosystem: networking
---

# cURL — 数据传输工具

## 它是什么

cURL（Client URL）是一个使用 URL 进行数据传输的命令行工具和库。它支持数十种协议，包括 HTTP、HTTPS、FTP、SFTP、SCP、LDAP 等。

## 安装

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## 基本用法

### GET 请求

```bash
curl https://api.github.com/users/octocat
```

### 带 JSON 的 POST

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### 将响应保存到文件

```bash
curl -o output.json https://api.example.com/data
```

### 跟随重定向

```bash
curl -L https://bit.ly/example
```

### 自定义标头

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## 关键选项

| 选项 | 描述 |
|------|------|
| `-X` | HTTP 方法（GET, POST, PUT, DELETE） |
| `-H` | 自定义标头 |
| `-d` | 请求体数据 |
| `-o` | 将输出写入文件 |
| `-L` | 跟随重定向 |
| `-v` | 详细模式 |
| `-s` | 静默模式（无进度） |
| `-k` | 允许不安全的 SSL |
| `-u` | 基本认证（user:password） |

## 最佳实践

- 在脚本中使用 `-sS` 来抑制进度但保留错误可见
- 使用 `--retry 3` 在网络失败时自动重试
- 切勿在 URL 中传递令牌；应使用 `Authorization` 标头代替